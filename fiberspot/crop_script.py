#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from fiberspot import example_script
from skimage import io
from skimage import color
from skimage.transform import resize

path_this_files_dir = os.path.realpath(os.path.dirname(__file__))

arguments = example_script.arguments
path = arguments["image_paths_and_boxes"]["specimen"]["path"]
box = arguments["image_paths_and_boxes"]["specimen"]["box"]


image = io.imread(path)
cropped = image[box[1] : box[3], box[0] : box[2]]

decreased_resolution = resize(
    cropped, (cropped.shape[0] // 4, cropped.shape[1] // 4), anti_aliasing=True
)

grey = color.rgb2gray(cropped)

io.imsave(
    os.path.join(os.path.dirname(path_this_files_dir), "data", "specimen" + ".png",),
    decreased_resolution,
)
