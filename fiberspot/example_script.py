#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import fiberspot

path_this_files_dir = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))

arguments = {
    "specimen": {
        "path": os.path.realpath(
            os.path.join(path_this_files_dir, "data", "example.jpg")
        ),
        "box": (1340, 360, 2700, 1700),  # Optional cropping
    },
    "neat_resin": {
        "path": os.path.realpath(
            os.path.join(path_this_files_dir, "data", "example.jpg")
        ),
        "box": (3230, 2220, 4650, 3550),  # Optional cropping
    },
    "radius": 60,  # pixel
    "average_volume_fraction_specimen": 0.27,  # dimensionless
    "plot": True,
    "plot_directory": os.path.join("plots", "example"),
}

if __name__ == "__main__":
    result = fiberspot.get_local_fiber_volume_fraction(arguments=arguments)
