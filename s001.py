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
from skimage import filters


def plot_segmentation(image, plot_directory):
    """
    https://scikit-image.org/docs/dev/auto_examples/segmentation/plot_chan_vese.html#sphx-glr-auto-examples-segmentation-plot-chan-vese-py
    """
    fig = plt.figure()

    plt.imshow(image)

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
image_array = np.array(specimen_grey)

critical_value = filters.threshold_otsu(image_array)
mask = np.array(specimen_grey) <= critical_value

plot_segmentation(image=mask, plot_directory=plot_directory)
