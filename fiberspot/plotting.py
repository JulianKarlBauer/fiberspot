#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import numpy as np


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
