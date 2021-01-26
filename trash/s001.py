#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate

# Bands: R, G, B, alpha
# Modes: RGB, L


directory = os.path.join("plots", "001")
os.makedirs(directory, exist_ok=True)

name_image = "IMG_9380.JPG"
path = os.path.realpath(os.path.join("data", name_image))
image = Image.open(path)

box = (300, 200, 900, 500)
region = image.crop(box)

os.makedirs("output", exist_ok=True)
region.save(
    os.path.splitext(os.path.realpath(os.path.join("output", name_image)))[0] + ".tiff"
)

red, green, blue = region.split()
luminance = region.copy().convert("L")

inverted = ImageOps.invert(luminance)
array = np.array(inverted)

########################################
# Plot bands
# Conclusion: Use luminance

if True:
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

########################################
# Grid
n_x, n_y = 10, 10
l_y, l_x = array.shape
start_x, start_y = l_x / (2.0 * n_x), l_y / (2.0 * n_y)
end_x, end_y = l_x - start_x, l_y - start_y
x = np.linspace(start_x, end_x, n_x)
y = np.linspace(start_y, end_y, n_y)
xx, yy = np.meshgrid(x, y)

########################################
# Plot grid
if True:
    plt.figure()
    plt.imshow(array)
    plt.scatter(xx, yy, marker="x", c="k")
    plt.title("Grid points")

    path_picture = os.path.join(directory, f"grid")
    plt.savefig(path_picture + ".png")
    plt.tight_layout()

########################################
# Local fiber volume content


class LocalFiberVolumeContent:
    def __init__(
        self, average_value, average_volume_content, neat_value, neat_volume_content=0,
    ):
        self.average_value = average_value
        self.average_volume_content = average_volume_content
        self.neat_value = neat_value
        self.neat_volume_content = neat_volume_content
        x = [neat_value, average_value]
        y = [neat_volume_content, average_volume_content]
        self.interpolation = scipy.interpolate.interp1d(x, y, fill_value="extrapolate")

    def __call__(self, value):
        return self.interpolation(value)


fvc_map = LocalFiberVolumeContent(
    average_value=np.mean(array), average_volume_content=0.27, neat_value=0
)

if True:
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


def create_circular_mask(h, w, center=None, radius=None):

    if center is None:  # use the middle of the image
        center = (int(w / 2), int(h / 2))
    if radius is None:  # use the smallest distance between the center and image walls
        radius = min(center[0], center[1], w - center[0], h - center[1])

    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - center[0]) ** 2 + (Y - center[1]) ** 2)

    mask = dist_from_center <= radius
    return mask


h, w = array.shape[:2]

if True:
    plt.figure()
    mask = np.full(array.shape, False)
    for i in range(n_x):
        for j in range(n_y):
            mask = mask | create_circular_mask(
                h, w, center=(xx[i, j], yy[i, j]), radius=25
            )
    tmp = array.copy()
    tmp[~mask] = 0
    plt.imshow(tmp)
    plt.title("Use circular mask")
    path_picture = os.path.join(directory, f"mask")
    plt.savefig(path_picture + ".png")
    plt.tight_layout()

means = np.zeros_like(xx)
fvcs = np.zeros_like(xx)
for i in range(10):
    for j in range(10):
        mask = create_circular_mask(h, w, center=(xx[i, j], yy[i, j]), radius=25)
        mean = array[mask].mean()
        means[i, j] = mean
        fvcs[i, j] = fvc_map(value=mean)


if True:
    plt.figure()
    plt.imshow(means)
    plt.colorbar()

    plt.title("Mean values")
    path_picture = os.path.join(directory, f"means")
    plt.savefig(path_picture + ".png")
    plt.tight_layout()


if True:
    plt.figure()
    plt.imshow(fvcs)
    plt.colorbar()

    plt.title("Fiber volume content")
    path_picture = os.path.join(directory, f"fvcs")
    plt.savefig(path_picture + ".png")
    plt.tight_layout()


# https://stackoverflow.com/questions/890051/how-do-i-generate-circular-thumbnails-with-pil
# https://stackoverflow.com/a/44874588/8935243
