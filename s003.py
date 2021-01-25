#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import numpy as np
import fiberspot


images = {
    "knips_04": {
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
    },
}

for key, properties in images.items():
    directory = os.path.join("plots", key)
    os.makedirs(directory, exist_ok=True)

    ########################################
    # Load image and reformat

    # Load
    raw_images = {
        key: fiberspot.load_and_convert_image(path=properties[key]["path"])
        for key in ["specimen", "neat_resin"]
    }

    # Crop
    images = {key: raw.crop(properties[key]["box"]) for key, raw in raw_images.items()}

    image_arrays = {key: np.array(image) for key, image in images.items()}

    # Plot
    fiberspot.plot_bands_of_image(
        path=properties["specimen"]["path"],
        box=properties["specimen"]["box"],
        plot_directory=directory,
    )

    ########################################
    # Grid
    grid_xx, grid_yy = fiberspot.get_regular_grid_on_image(
        array=image_arrays["specimen"]
    )

    # Plot
    fiberspot.plot_grid(
        array=image_arrays["specimen"],
        grid_xx=grid_xx,
        grid_yy=grid_yy,
        plot_directory=directory,
    )

    ########################################
    # Local fiber volume content
    fvc_map = fiberspot.LocalFiberVolumeContentMap(
        average_grey=np.mean(image_arrays["specimen"]),
        average_volume_content=properties["average_volume_content_specimen"],
        neat_grey=np.mean(image_arrays["neat_resin"]),
    )

    # Plot
    fiberspot.plot_fiber_volume_content(fvc_map, plot_directory=directory)

    ########################################
    # Create masks and calc local fiber volume content on specific areas

    radius = properties["radius"]
    fiberspot.plot_mask(
        array=image_arrays["specimen"],
        grid_xx=grid_xx,
        grid_yy=grid_yy,
        radius=radius,
        plot_directory=directory,
    )

    means = np.zeros_like(grid_xx)
    fvcs = np.zeros_like(grid_xx)
    for i in range(10):
        for j in range(10):
            mask = fiberspot.create_single_circular_mask(
                image_shape_2D=image_arrays["specimen"].shape[:2],
                center=(grid_xx[i, j], grid_yy[i, j]),
                radius=radius,
            )
            mean = image_arrays["specimen"][mask].mean()
            means[i, j] = mean
            fvcs[i, j] = fvc_map(value=mean)

    fiberspot.plot_image(
        image=means, title="Mean values", path=os.path.join(directory, "means" + ".png")
    )
    fiberspot.plot_image(
        image=fvcs,
        title="Fiber volume content",
        path=os.path.join(directory, "fvcs" + ".png"),
    )
