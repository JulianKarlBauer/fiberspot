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


class LocalFiberVolumeContentMap:
    def __init__(
        self, average_grey, average_volume_content, neat_grey, neat_volume_content=0,
    ):
        self.average_grey = average_grey
        self.average_volume_content = average_volume_content
        self.neat_grey = neat_grey
        self.neat_volume_content = neat_volume_content

        x = [neat_grey, average_grey]
        y = [neat_volume_content, average_volume_content]

        self.interpolate = scipy.interpolate.interp1d(x, y, fill_value="extrapolate")

    def __call__(self, value):
        return self.interpolate(value)


def get_local_fiber_volume_content(arguments):
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
    # Local fiber volume content
    fvc_map = fiberspot.LocalFiberVolumeContentMap(
        average_grey=np.mean(image_arrays["specimen"]),
        average_volume_content=arguments["average_volume_content_specimen"],
        neat_grey=np.mean(image_arrays["neat_resin"]),
    )

    if plot:
        fiberspot.plotting.plot_fiber_volume_content(fvc_map, plot_directory=directory)

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

        mean_values[filter_key] = mean = filter_function(image_arrays["specimen"])

        if plot:
            fiberspot.plotting.plot_image(
                image=mean,
                title="Mean values",
                path=os.path.join(directory, "means" + "_" + filter_key + ".png"),
            )

    ########################################
    # Map mean onto fiber volume content
    fiber_volume_content = {}
    for filter_key, filter in available_filter_functions.items():

        fiber_volume_content[filter_key] = fvc = fvc_map(
            np.array(mean_values[filter_key])
        )

        if plot:
            fiberspot.plotting.plot_image(
                image=fvc,
                title="Fiber volume content",
                path=os.path.join(directory, "fvcs" + "_" + filter_key + ".png"),
            )

    return {"mean": mean_values, "fiber_volume_content": fiber_volume_content}
