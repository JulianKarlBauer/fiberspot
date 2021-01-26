#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate
import fiberspot


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


def get_regular_grid_on_image(array):
    n_x, n_y = 10, 10
    l_y, l_x = array.shape
    start_x, start_y = l_x / (2.0 * n_x), l_y / (2.0 * n_y)
    end_x, end_y = l_x - start_x, l_y - start_y
    x = np.linspace(start_x, end_x, n_x)
    y = np.linspace(start_y, end_y, n_y)
    xx, yy = np.meshgrid(x, y)
    return xx, yy


def plot_grid(array, grid_xx, grid_yy, plot_directory):
    fig = plt.figure()
    plt.imshow(array)
    plt.scatter(grid_xx, grid_yy, marker="x", c="k")
    plt.title("Grid points")

    path_picture = os.path.join(plot_directory, f"grid")
    plt.savefig(path_picture + ".png")
    plt.tight_layout()
    plt.close(fig)


def plot_fiber_volume_content(fvc_map, plot_directory):
    fig = plt.figure()
    x = np.linspace(0, 256, 300)
    y = fvc_map(value=x)
    plt.plot(x, y)
    plt.xlabel("Grey value")
    plt.ylabel("Fiber volume content")
    plt.title("Get fiber volume content from grey value")

    path_picture = os.path.join(plot_directory, f"fvc")
    plt.savefig(path_picture + ".png")
    plt.tight_layout()
    plt.close(fig)


def create_single_circular_mask(image_shape_2D, center=None, radius=None):
    """This is highly inefficient and kind of stupid..."""
    Y, X = np.ogrid[: image_shape_2D[0], : image_shape_2D[1]]
    dist_from_center = np.sqrt((X - center[0]) ** 2 + (Y - center[1]) ** 2)

    mask = dist_from_center <= radius
    return mask


def plot_mask(array, grid_xx, grid_yy, radius, plot_directory):
    array_shape = array.shape[:2]
    fig = plt.figure()
    mask = np.full(array_shape, False)
    for i in range(grid_xx.shape[0]):
        for j in range(grid_xx.shape[1]):
            mask = mask | create_single_circular_mask(
                image_shape_2D=array_shape[:2],
                center=(grid_xx[i, j], grid_yy[i, j]),
                radius=radius,
            )
    tmp = array.copy()
    tmp[~mask] = 0
    plt.imshow(tmp)
    plt.title("Use circular mask")
    path_picture = os.path.join(plot_directory, f"mask")
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

    directory = arguments["plot_directory"]
    os.makedirs(directory, exist_ok=True)

    plot = arguments["plot"]

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

    # Plot
    if plot:
        fiberspot.plot_bands_of_image(
            path=arguments["specimen"]["path"],
            box=arguments["specimen"]["box"],
            plot_directory=directory,
        )

    ########################################
    # Grid
    grid_xx, grid_yy = fiberspot.get_regular_grid_on_image(
        array=image_arrays["specimen"]
    )

    # Plot
    if plot:
        fiberspot.plot_grid(
            array=image_arrays["specimen"],
            grid_xx=grid_xx,
            grid_yy=grid_yy,
            plot_directory=directory,
        )

    ########################################
    # Local fiber volume content
    fvc_map = fiberspot.LocalFiberVolumeContentMap(
        average_grey=np.mean(image_arrays["specimen"]),
        average_volume_content=arguments["average_volume_content_specimen"],
        neat_grey=np.mean(image_arrays["neat_resin"]),
    )

    # Plot
    if plot:
        fiberspot.plot_fiber_volume_content(fvc_map, plot_directory=directory)

    ########################################
    # Create masks and calc local fiber volume content on specific areas

    radius = arguments["radius"]
    if plot:
        fiberspot.plot_mask(
            array=image_arrays["specimen"],
            grid_xx=grid_xx,
            grid_yy=grid_yy,
            radius=radius,
            plot_directory=directory,
        )

    mean_values_inside_masks = np.zeros_like(grid_xx)
    fvc_inside_masks = np.zeros_like(grid_xx)
    for i in range(10):
        for j in range(10):
            mask = fiberspot.create_single_circular_mask(
                image_shape_2D=image_arrays["specimen"].shape[:2],
                center=(grid_xx[i, j], grid_yy[i, j]),
                radius=radius,
            )
            mean = image_arrays["specimen"][mask].mean()
            mean_values_inside_masks[i, j] = mean
            fvc_inside_masks[i, j] = fvc_map(value=mean)

    if plot:
        fiberspot.plot_image(
            image=mean_values_inside_masks,
            title="Mean values",
            path=os.path.join(directory, "means" + ".png"),
        )
        fiberspot.plot_image(
            image=fvc_inside_masks,
            title="Fiber volume content",
            path=os.path.join(directory, "fvcs" + ".png"),
        )
    return fvc_inside_masks