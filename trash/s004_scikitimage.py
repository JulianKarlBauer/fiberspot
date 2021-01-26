#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import skimage
from skimage import io

directory = os.path.join("plots", "004")
os.makedirs(directory, exist_ok=True)

path = os.path.realpath(os.path.join("data", "knips_04", "SpecimenAndPureresin.JPG"))

# from skimage import data
# from skimage.morphology import disk
# from skimage.filters import rank
#
# image = data.coins()
# selem = disk(20)
#
# percentile_result = rank.mean_percentile(image, selem=selem, p0=0.1, p1=0.9)
# bilateral_result = rank.mean_bilateral(image, selem=selem, s0=500, s1=500)
# normal_result = rank.mean(image, selem=selem)

image = io.imread(path)

gray_values = skimage.color.rgb2gray(image)
