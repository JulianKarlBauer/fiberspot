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
from skimage.segmentation import chan_vese

arguments = example_script.arguments

original = Image.open(arguments["specimen"]["path"])
specimen = original.crop(box=arguments["specimen"]["box"])
specimen_grey = ImageOps.invert(specimen.convert("L"))
image_array = img_as_float(specimen_grey)

segmentation_result = chan_vese(
    image_array,
    mu=0.25,
    lambda1=1,
    lambda2=1,
    tol=1e-3,
    max_iter=200,
    dt=0.5,
    init_level_set="checkerboard",
    extended_output=True,
)


fig, axes = plt.subplots(2, 2, figsize=(8, 8))
ax = axes.flatten()

ax[0].imshow(image_array, cmap="gray")
ax[0].set_axis_off()
ax[0].set_title("Original Image", fontsize=12)

ax[1].imshow(segmentation_result[0], cmap="gray")
ax[1].set_axis_off()
title = "Chan-Vese segmentation - {} iterations".format(len(segmentation_result[2]))
ax[1].set_title(title, fontsize=12)

ax[2].imshow(segmentation_result[1], cmap="gray")
ax[2].set_axis_off()
ax[2].set_title("Final Level Set", fontsize=12)

ax[3].plot(segmentation_result[2])
ax[3].set_title("Evolution of energy over iterations", fontsize=12)

fig.tight_layout()
