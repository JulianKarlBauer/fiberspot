#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import fiberspot

path_this_files_dir = os.path.realpath(os.path.dirname(__file__))
main_dir = os.path.dirname(path_this_files_dir)

arguments = {
    "image_paths_and_boxes": {
        "specimen": {
            "path": os.path.realpath(os.path.join(main_dir, "data", "example.jpg")),
            "box": (1340, 360, 2700, 1700),  # Optional cropping
        },
        "neat_resin": {
            "path": os.path.realpath(os.path.join(main_dir, "data", "example.jpg")),
            "box": (3230, 2220, 4650, 3550),  # Optional cropping
        },
    },
    "radius": 60,  # pixel
    "filter_key": "all",
    "average_volume_fraction_specimen": 0.27,  # dimensionless
    "plot": True,
    "plot_directory": os.path.join("plots", "example"),
}

if __name__ == "__main__":

    result = fiberspot.get_local_fiber_volume_fraction_from_images(**arguments)
