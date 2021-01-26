#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate
import fiberspot
from PIL import ImageFilter


def load_and_convert_image(path):
    # Load image
    raw_image = Image.open(path)
    # Convert part of image to useful data type
    return ImageOps.invert(raw_image.convert("L"))


def plot_bands_of_image(path, box, plot_directory):
    """
    Plot bands
    Conclusion: Use luminance
    """

    # Bands: R, G, B, alpha
    # Modes: RGB, L

    raw_image = Image.open(path)

    region = raw_image.crop(box)

    red, green, blue = region.split()
    luminance = region.copy().convert("L")

    inverted = ImageOps.invert(luminance)
    array = np.array(inverted)

    aspect_ratio = array.shape[0] / array.shape[1]
    fig, axs = plt.subplots(3, 2, figsize=(2 * 6, 3 * 6 * aspect_ratio))
    subplots = {
        "RGB": {"image": region, "ax": axs[0, 0]},
        "Red": {"image": red, "ax": axs[0, 1]},
        "Green": {"image": green, "ax": axs[1, 0]},
        "Blue": {"image": blue, "ax": axs[1, 1]},
        "Luminance": {"image": luminance, "ax": axs[2, 0]},
        "Inverted luminance": {"image": inverted, "ax": axs[2, 1]},
    }

    for key_sub, data_sub in subplots.items():
        ax = data_sub["ax"]
        ax.imshow(data_sub["image"])
        ax.set_title(key_sub)

    path_picture = os.path.join(plot_directory, f"modes")
    plt.savefig(path_picture + ".png")
    plt.tight_layout()
    plt.close(fig)


def plot_fiber_volume_content(fvc_map, plot_directory):
    fig = plt.figure()
    x = np.linspace(0, 256, 300)
    y = fvc_map(value=x)

    args = dict(linewidth=4, markersize=12)

    plt.plot(
        fvc_map.average_grey,
        fvc_map.average_volume_content,
        "rs",
        label="Average over specimen",
        **args,
    )
    plt.plot(
        fvc_map.neat_grey, fvc_map.neat_volume_content, "go", label="Neat resin", **args
    )
    plt.plot(x, y)
    plt.xlabel("Grey value")
    plt.ylabel("Fiber volume content")
    plt.grid()
    plt.legend()

    path_picture = os.path.join(plot_directory, f"fvc")
    plt.savefig(path_picture + ".png")
    plt.tight_layout()
    plt.close(fig)


def plot_image(image, title, path):
    fig = plt.figure()
    plt.imshow(image)
    plt.colorbar()

    plt.title(title)
    plt.savefig(path)
    plt.tight_layout()
    plt.close(fig)


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
        fiberspot.plot_bands_of_image(
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
        fiberspot.plot_fiber_volume_content(fvc_map, plot_directory=directory)

    ########################################
    # Use filter to calc mean and map mean onto fiber volume content

    radius = arguments["radius"]

    available_filters = {
        "box": ImageFilter.BoxBlur(radius=radius),
        "gaussian": ImageFilter.GaussianBlur(radius=radius),
    }

    mean_values = {}
    fiber_volume_content = {}
    for filter_key, filter in available_filters.items():

        mean_values[filter_key] = mean = images["specimen"].filter(filter)
        fiber_volume_content[filter_key] = fvc = fvc_map(np.array(mean))

        if plot:
            plot_image(
                image=mean,
                title="Mean values",
                path=os.path.join(directory, "means" + "_" + filter_key + ".png"),
            )
            plot_image(
                image=fvc,
                title="Fiber volume content",
                path=os.path.join(directory, "fvcs" + "_" + filter_key + ".png"),
            )

    return {"mean": mean_values, "fiber_volume_content": fiber_volume_content}
