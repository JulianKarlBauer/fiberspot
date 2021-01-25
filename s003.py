#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate

# Bands: R, G, B, alpha
# Modes: RGB, L


def load_and_convert_image(path):
    # Load image
    raw_image = Image.open(path)
    # Convert part of image to useful data type
    return ImageOps.invert(raw_image.convert("L"))


def plot_bands_of_image(path, box):
    """
    Plot bands
    Conclusion: Use luminance
    """

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

    path_picture = os.path.join(directory, f"modes")
    plt.savefig(path_picture + ".png")
    plt.tight_layout()
    plt.close(fig)


def get_regular_grid_on_image(array):
    n_x, n_y = 10, 10
    l_y, l_x = array.shape
    start_x, start_y = l_x / (2.0 * n_x), l_y / (2.0 * n_y)
    end_x, end_y = l_x - start_x, l_y - start_y
    x = np.linspace(start_x, end_x, n_x)
    y = np.linspace(start_y, end_y, n_y)
    xx, yy = np.meshgrid(x, y)
    return xx, yy


def plot_grid(array, grid_xx, grid_yy):
    plt.figure()
    plt.imshow(array)
    plt.scatter(grid_xx, grid_yy, marker="x", c="k")
    plt.title("Grid points")

    path_picture = os.path.join(directory, f"grid")
    plt.savefig(path_picture + ".png")
    plt.tight_layout()


def plot_fiber_volume_content(fvc_map):
    plt.figure()
    x = np.linspace(0, 256, 300)
    y = fvc_map(value=x)
    plt.plot(x, y)
    plt.xlabel("Grey value")
    plt.ylabel("Fiber volume content")
    plt.title("Get fiber volume content from grey value")

    path_picture = os.path.join(directory, f"fvc")
    plt.savefig(path_picture + ".png")
    plt.tight_layout()


def create_single_circular_mask(image_shape_2D, center=None, radius=None):
    """This is highly inefficient and kind of stupid..."""
    Y, X = np.ogrid[: image_shape_2D[0], : image_shape_2D[1]]
    dist_from_center = np.sqrt((X - center[0]) ** 2 + (Y - center[1]) ** 2)

    mask = dist_from_center <= radius
    return mask


def plot_mask(array, grid_shape):
    array_shape = array.shape[:2]
    plt.figure()
    mask = np.full(array_shape, False)
    for i in range(grid_shape[0]):
        for j in range(grid_shape[1]):
            mask = mask | create_single_circular_mask(
                image_shape_2D=array_shape[:2],
                center=(grid_xx[i, j], grid_yy[i, j]),
                radius=radius,
            )
    tmp = array.copy()
    tmp[~mask] = 0
    plt.imshow(tmp)
    plt.title("Use circular mask")
    path_picture = os.path.join(directory, f"mask")
    plt.savefig(path_picture + ".png")
    plt.tight_layout()


def plot_image(image, title, path):
    fig = plt.figure()
    plt.imshow(image)
    plt.colorbar()

    plt.title(title)
    plt.savefig(path)
    plt.tight_layout()
    plt.close(fig)


class LocalFiberVolumeContent:
    def __init__(
        self, average_grey, average_volume_content, neat_grey, neat_volume_content=0,
    ):
        self.average_grey = average_grey
        self.average_volume_content = average_volume_content
        self.neat_grey = neat_grey
        self.neat_volume_content = neat_volume_content

        x = [neat_grey, average_grey]
        y = [neat_volume_content, average_volume_content]

        self.interpolation = scipy.interpolate.interp1d(x, y, fill_value="extrapolate")

    def __call__(self, value):
        return self.interpolation(value)


images = {
    "knips_04": {
        "path_specimen": os.path.realpath(
            os.path.join("data", "knips_04", "SpecimenAndPureresin.JPG")
        ),
        "box_specimen": (1340, 360, 2700, 1700),
        "path_neat_resin": os.path.realpath(
            os.path.join("data", "knips_04", "SpecimenAndPureresin.JPG")
        ),
        "box_neat_resin": (3230, 2220, 4650, 3550),
        "radius": 60,
    },
}

for key, properties in images.items():
    directory = os.path.join("plots", key)
    os.makedirs(directory, exist_ok=True)

    ########################################
    # Select image and convert

    # Load
    raw_image = load_and_convert_image(path=properties["path_specimen"])

    # Select part of image
    box = properties["box_specimen"]

    image = raw_image.crop(box)
    image_array = np.array(image)

    # Plot
    plot_bands_of_image(
        path=properties["path_specimen"], box=properties["box_specimen"]
    )

    ########################################
    # Grid
    grid_xx, grid_yy = get_regular_grid_on_image(array=image_array)

    # Plot
    plot_grid(array=image_arrays["specimen"], grid_xx=grid_xx, grid_yy=grid_yy)

    ########################################
    # Local fiber volume content
    fvc_map = LocalFiberVolumeContent(
        average_grey=np.mean(image_array), average_volume_content=0.27, neat_grey=0
    )

    # Plot
    plot_fiber_volume_content(fvc_map)

    ########################################
    # Create masks and calc local fiber volume content on specific areas

    radius = properties["radius"]
    plot_mask(array=image_array, grid_shape=grid_xx.shape)

    means = np.zeros_like(grid_xx)
    fvcs = np.zeros_like(grid_xx)
    for i in range(10):
        for j in range(10):
            mask = create_single_circular_mask(
                image_shape_2D=image_array.shape[:2],
                center=(grid_xx[i, j], grid_yy[i, j]),
                radius=radius,
            )
            mean = image_array[mask].mean()
            means[i, j] = mean
            fvcs[i, j] = fvc_map(value=mean)

    plot_image(
        image=means, title="Mean values", path=os.path.join(directory, "means" + ".png")
    )
    plot_image(
        image=fvcs,
        title="Fiber volume content",
        path=os.path.join(directory, "fvcs" + ".png"),
    )
