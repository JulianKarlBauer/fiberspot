#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools

setuptools.setup(
    name="fiberspot",
    version="0.0.1",
    author="Julian Bauer",
    author_email="julian.bauer@kit.edu",
    description="Spot fiber properties on 2D optical images",
    url="https://git.scc.kit.edu/julian_/fiberspot",
    packages=["fiberspot"],
    package_dir={"fiberspot": "fiberspot"},
    # package_data={
    #     "fiberspot": package_files(
    #         directory=os.path.realpath(
    #             os.path.join(
    #                 os.path.dirname(os.path.realpath(__file__)), "fiberspot", "data"
    #             )
    #         )
    #     )
    # },
    # entry_points={
    #     "console_scripts": [
    #         "export_data_sets_to_file = fiberspot.scripts:export_data_sets_to_file",
    #     ]
    # },
    # include_package_data=True,
    install_requires=["numpy", "matplotlib", "pillow", "scipy"],
    # extras_require={":python_version>'3.5'": ["natsort", "matplotlib"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)

# import os
#
#
# def package_files(directory, exclude_pattern="__pycache__"):
#     paths = []
#     for (path, directories, filenames) in os.walk(directory):
#         for filename in filenames:
#             if exclude_pattern not in path:
#                 paths.append(os.path.join("..", path, filename))
#     return paths
