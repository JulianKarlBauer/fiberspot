#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate
from skimage import img_as_float
import fiberspot
from fiberspot import example_script
from skimage.segmentation import chan_vese, morphological_chan_vese
from skimage import segmentation


def plot_segmentation(segmentation_result, image_array, plot_directory):
    """
    https://scikit-image.org/docs/dev/auto_examples/segmentation/plot_chan_vese.html#sphx-glr-auto-examples-segmentation-plot-chan-vese-py
    """
    fig, axes = plt.subplots(2, 2, figsize=(8, 8))
    ax = axes.flatten()

    ax[0].imshow(image_array, cmap="gray")
    ax[0].set_axis_off()
    ax[0].set_title("Original Image", fontsize=12)

    ax[1].imshow(segmentation_result, cmap="gray")
    ax[1].set_axis_off()

    fig.tight_layout()
    path_picture = os.path.join(plot_directory, f"segmentation")
    plt.savefig(path_picture + ".png")
    plt.close(fig)


path_this_files_dir = os.path.realpath(os.path.dirname(__file__))
plot_directory = os.path.join(path_this_files_dir, "plots")

arguments = example_script.arguments

original = Image.open(arguments["specimen"]["path"])
specimen = original.crop(box=arguments["specimen"]["box"])
specimen_grey = ImageOps.invert(specimen.convert("L"))
image_array = img_as_float(specimen_grey)
#
# segmentation_result = chan_vese(
#     image_array,
#     mu=0.7,
#     lambda1=1.1,
#     lambda2=0.9,
#     tol=1e-3,
#     max_iter=200,
#     dt=0.2,
#     init_level_set="checkerboard",
#     extended_output=True,
# )

initial_level_set = np.zeros(image_array.shape)
initial_level_set[[0, -1], :] = 1
initial_level_set[:, [0, -1]] = 1
segmentation_result = morphological_chan_vese(
    image_array, 35, init_level_set=initial_level_set, smoothing=3
)


plot_segmentation(segmentation_result, image_array, plot_directory)
