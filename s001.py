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
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig = plt.figure()

    plt.imshow(image)
    plt.colorbar()

    fig.tight_layout()
    # path_picture = os.path.join(plot_directory, f"segmentation")
    plt.savefig(path + ".png")
    plt.close(fig)


path_this_files_dir = os.path.realpath(os.path.dirname(__file__))
plot_directory = os.path.join(path_this_files_dir, "plots", "s001")

arguments = example_script.arguments

original = Image.open(arguments["image_paths_and_boxes"]["specimen"]["path"])
specimen = original.crop(box=arguments["image_paths_and_boxes"]["specimen"]["box"])
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
    "gaussian_skimage": lambda x: skimage.filters.gaussian(x, sigma=1),
}

mean_values = {}
for filter_key, filter_function in available_filter_functions.items():
    mean_values[filter_key] = filter_function(image_array)

    plot_image(
        image=mean_values[filter_key],
        path=os.path.join(plot_directory, "filter_" + filter_key),
    )

skimage.filters.rank.mean(image_array, skimage.morphology.disk(radius))

img = image_array
blur = 3

area_threshold = 500
mask_morph_closing = skimage.morphology.area_closing(
    mask, area_threshold=60  # , selem=skimage.morphology.square(1)
)
mask_moph_close_then_open = skimage.morphology.opening(
    mask_morph_closing, selem=skimage.morphology.square(20)
)

mask_morph_opening = skimage.morphology.opening(mask)

mask_area_closing = ~skimage.morphology.area_closing(
    ~mask, area_threshold=area_threshold
)
mask_close_01 = ~skimage.morphology.remove_small_holes(
    ~mask, area_threshold=area_threshold
)
mask_close_02 = skimage.morphology.remove_small_holes(
    mask_close_01, area_threshold=area_threshold
)
mask = mask_moph_close_then_open.astype(float)

# img = image_array.astype(float)
img = img_as_float(image_array)


# normalized convolution of image with mask
img_times_mask = img * mask
filter = scipy.ndimage.filters.gaussian_filter(img * mask, sigma=blur)
foulded = filter.copy()
weights = scipy.ndimage.filters.gaussian_filter(mask, sigma=blur)
filter /= weights
# after normalized convolution, you can choose to delete any data outside the mask:
# filter *= mask
# filter_nonan = np.nan_to_num(filter, nan=0.0)


def my_filter(array):
    radius = 60
    return skimage.filters.rank.mean(array, skimage.morphology.square(2 * radius))


def normalized_convolution_skimage(img, mask):
    img = img_as_float(img)
    mask = img_as_float(mask)
    array = img_as_float(my_filter(img * mask))
    weights = img_as_float(my_filter(mask))
    array /= weights
    return skimage.img_as_ubyte(array)


normalized_skimage = normalized_convolution_skimage(img=img, mask=mask)


for key, var in {
    "mask_moph_close_then_open": mask_moph_close_then_open,
    "mask_morph_closing": mask_morph_closing,
    "mask_morph_opening": mask_morph_opening,
    "mask_close_01": mask_close_01,
    "mask_close_02": mask_close_02,
    "mask_area_closing": mask_area_closing,
    "filter": filter,
    "filter_normalized_skimage": normalized_skimage,
    "weights": weights,
    "img_times_mask": img_times_mask,
    "mask": mask,
    "img": img,
    "foulded": foulded,
}.items():
    plot_image(
        image=var, path=os.path.join(plot_directory, "normalized_convolution", key)
    )


# mean_values = {}
# for filter_key, filter in available_filters.items():
#     mean_values[filter_key] = specimen_grey.filter(filter)
#
#     plot_image(
#         image=mean_values[filter_key],
#         path=os.path.join(plot_directory, "filter" + filter_key),
#     )
