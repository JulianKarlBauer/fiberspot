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
import os
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate
import fiberspot
from PIL import ImageFilter
import skimage


def plot_image(image, path):
    """
    https://scikit-image.org/docs/dev/auto_examples/segmentation/plot_chan_vese.html#sphx-glr-auto-examples-segmentation-plot-chan-vese-py
    """
    fig = plt.figure()

    plt.imshow(image)
    plt.colorbar()

    fig.tight_layout()
    # path_picture = os.path.join(plot_directory, f"segmentation")
    plt.savefig(path + ".png")
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

plot_image(image=mask, path=os.path.join(plot_directory, "segmentation"))


radius = 50

available_filter_functions = {
    "box_PIL": lambda x: getattr(Image.fromarray(x), "filter").__call__(
        ImageFilter.BoxBlur(radius=radius)
    ),
    "gaussian_PIL": lambda x: getattr(Image.fromarray(x), "filter").__call__(
        ImageFilter.GaussianBlur(radius=radius)
    ),
    "mean_disk": lambda x: skimage.filters.rank.mean(
        x, skimage.morphology.disk(radius)
    ),
    "mean_square": lambda x: skimage.filters.rank.mean(
        x, skimage.morphology.square(2 * radius)
    ),
}

mean_values = {}
for filter_key, filter_function in available_filter_functions.items():
    mean_values[filter_key] = filter_function(image_array)
    plot_image(
        image=mean_values[filter_key],
        path=os.path.join(plot_directory, "filter_" + filter_key),
    )

import skimage

skimage.filters.rank.mean(image_array, skimage.morphology.disk(radius))

# mean_values = {}
# for filter_key, filter in available_filters.items():
#     mean_values[filter_key] = specimen_grey.filter(filter)
#
#     plot_image(
#         image=mean_values[filter_key],
#         path=os.path.join(plot_directory, "filter" + filter_key),
#     )
