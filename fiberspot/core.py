#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from PIL import Image, ImageOps
import numpy as np
import scipy.interpolate
import fiberspot
from PIL import ImageFilter
import skimage
from skimage import filters


def load_and_convert_image(path):
    # Load image
    raw_image = Image.open(path)
    # Convert part of image to useful data type
    return ImageOps.invert(raw_image.convert("L"))


class LocalFiberVolumeFractionMap:
    def __init__(
        self, average_grey, average_volume_fraction, neat_grey, neat_volume_fraction=0,
    ):
        self.average_grey = average_grey
        self.average_volume_fraction = average_volume_fraction
        self.neat_grey = neat_grey
        self.neat_volume_fraction = neat_volume_fraction

        x = [neat_grey, average_grey]
        y = [neat_volume_fraction, average_volume_fraction]

        self.interpolate = scipy.interpolate.interp1d(x, y, fill_value="extrapolate")

    def __call__(self, value):
        return self.interpolate(value)


def get_mask_for_example_image(image_array):
    image_array = skimage.img_as_float(image_array)
    critical_value = skimage.filters.threshold_otsu(image_array)
    mask = image_array <= critical_value
    mask_morph_closing = skimage.morphology.area_closing(mask, area_threshold=60)
    return skimage.morphology.opening(
        mask_morph_closing, selem=skimage.morphology.square(20)
    )


def normalized_convolution_skimage(img, mask, filter_function):
    img = skimage.img_as_float(img)
    mask = skimage.img_as_float(mask)
    array = skimage.img_as_float(filter_function(skimage.img_as_ubyte(img * mask)))
    weights = skimage.img_as_float(filter_function(skimage.img_as_ubyte(mask)))
    array /= weights
    return skimage.img_as_ubyte(array)


def get_local_fiber_volume_fraction(arguments):
    plot = arguments["plot"]

    if plot:
        directory = arguments["plot_directory"]
        os.makedirs(directory, exist_ok=True)

    ########################################
    # Load image and reformat

    # Load
    raw_images = {
        key: fiberspot.load_and_convert_image(path=arguments[key]["path"])
        for key in ["specimen", "neat_resin"]
    }

    # Crop
    images = {
        key: raw.crop(box=arguments[key]["box"]) if "box" in arguments[key] else raw
        for key, raw in raw_images.items()
    }

    image_arrays = {key: np.array(image) for key, image in images.items()}

    if plot:
        fiberspot.plotting.plot_bands_of_image(
            path=arguments["specimen"]["path"],
            box=arguments["specimen"]["box"],
            plot_directory=directory,
        )

    ########################################
    # Get mask
    if False:
        mask = get_mask_for_example_image(image_array=image_arrays["specimen"])
    else:
        mask = np.full(image_arrays["specimen"].shape, True)

    if plot:
        fiberspot.plotting.plot_image(
            image=mask, title="Mask", path=os.path.join(directory, "mask" + ".png"),
        )

    ########################################
    # Local fiber volume content
    fvc_map = fiberspot.LocalFiberVolumeFractionMap(
        average_grey=np.mean(image_arrays["specimen"]),
        average_volume_fraction=arguments["average_volume_fraction_specimen"],
        neat_grey=np.mean(image_arrays["neat_resin"]),
    )

    if plot:
        fiberspot.plotting.plot_fiber_volume_fraction(fvc_map, plot_directory=directory)

    ########################################
    # Define bunch of filters
    radius = arguments["radius"]

    available_filter_functions = {
        "box_PIL": lambda x: getattr(Image.fromarray(x), "filter").__call__(
            ImageFilter.BoxBlur(radius=radius)
        ),
        "gaussian_PIL": lambda x: getattr(Image.fromarray(x), "filter").__call__(
            ImageFilter.GaussianBlur(radius=radius)
        ),
        "mean_disk_skimage": lambda x: skimage.filters.rank.mean(
            x, skimage.morphology.disk(radius)
        ),
        "mean_square_skimage": lambda x: skimage.filters.rank.mean(
            x, skimage.morphology.square(2 * radius)
        ),
        "gaussian_skimage": lambda x: skimage.filters.gaussian(x, sigma=radius),
    }

    ########################################
    # Use filter to calc mean
    mean_values = {}
    for filter_key, filter_function in available_filter_functions.items():

        mean_values[filter_key] = mean = normalized_convolution_skimage(
            img=image_arrays["specimen"], mask=mask, filter_function=filter_function
        )

        if plot:
            fiberspot.plotting.plot_image(
                image=mean,
                title="Mean values",
                path=os.path.join(directory, "means" + "_" + filter_key + ".png"),
            )

    ########################################
    # Map mean onto fiber volume content
    fiber_volume_fraction = {}
    for filter_key, filter in available_filter_functions.items():

        fiber_volume_fraction[filter_key] = fvc = fvc_map(
            np.array(mean_values[filter_key])
        )

        if plot:
            fiberspot.plotting.plot_image(
                image=fvc,
                title="Fiber volume fraction",
                path=os.path.join(directory, "fvcs" + "_" + filter_key + ".png"),
            )

    return {"mean": mean_values, "fiber_volume_fraction": fiber_volume_fraction}
