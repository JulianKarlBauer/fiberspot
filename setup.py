#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools

setuptools.setup(
    name="fiberspot",
    version="0.0.1",
    author="Julian Bauer",
    author_email="juliankarlbauer@gmx.de",
    description="Spot fiber properties on 2D optical images",
    url="https://git.scc.kit.edu/julian_/fiberspot",
    packages=["fiberspot"],
    package_dir={"fiberspot": "fiberspot"},
    install_requires=[
        "numpy",
        "matplotlib",
        "pillow",
        "scipy",
        "pytest",
        "scikit-image",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
