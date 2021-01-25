#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import fiberspot


images = {
    "example": {
        "specimen": {
            "path": os.path.realpath(os.path.join("data", "example.JPG")),
            "box": (1340, 360, 2700, 1700),
        },
        "neat_resin": {
            "path": os.path.realpath(os.path.join("data", "example.JPG")),
            "box": (3230, 2220, 4650, 3550),
        },
        "radius": 60,
        "average_volume_content_specimen": 0.27,
        "plot": True,
        "plot_directory": os.path.join("plots", "example"),
    },
}


fiberspot.get_local_fiber_volume_content(properties=images["example"])
