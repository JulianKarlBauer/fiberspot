[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![LICENSE](https://black.readthedocs.io/en/stable/_static/license.svg)](https://raw.github.com/nilsmeyerkit/fiberoripy/master/LICENSE)
![Python package](https://github.com/JulianKarlBauer/fiberspot_private/workflows/Python%20package/badge.svg)
[![DOI](https://zenodo.org/badge/333071299.svg)](https://zenodo.org/badge/latestdoi/333071299)

# fiberspot

Identify fiber properties on 2D optical images.  
See [license](https://github.com/JulianKarlBauer/fiberspot/blob/main/LICENSE) and
[cite as](https://zenodo.org/record/4471261/export/hx#.YBFCgtYo-Ts)

```bibtex
@software{juliankarlbauer_2021_4471261,
  author       = {JulianKarlBauer},
  title        = {JulianKarlBauer/fiberspot: Prototype},
  month        = jan,
  year         = 2021,
  publisher    = {Zenodo},
  version      = {v0.0.1},
  doi          = {10.5281/zenodo.4471261},
  url          = {https://doi.org/10.5281/zenodo.4471261}
}
```

**Call for application**:
If you have data sets you would like to analyze, please contact me or
think about opening an issue.

**[Additional features](#unpublished-features)**:
are already available in a private project, e.g.

- Masking features inside an image by image segmentation
- Weighted / normalized convolution filtering

---

## Local Fiber Volume fraction

The algorithm described here is very simple.
Applicability is not proven and potential problems are discussed below.

### Motivation

Local fiber volume fraction is the fiber orientation information of zeroth order.
Spatial variance of fiber volume fraction is an inherent property of inhomogeneous
materials.
Accurate determination of local mechanical properties by e.g. homogenization schemes
requires knowledge on the local fiber volume fraction.

Local fiber volume fraction can be determined by analyzing reflection and
distraction of radiation as e.g. x-rays.

Optical measurements, i.e. images taken with conventional cameras, are

- Availabile
- Cheap
- Flexible
- And offer high resolution.

If a flat, shell-like specimen is illuminated from one side and the transmitted
light intensity is measured by on optical sensor (camera) from the other side, we call
the resulting image an radiography image.

This package maps light intensity of radiography images to local fiber volume fraction.
The key idea can be used for any heterogeneous materials consisting of phases with
differing transparency or noticeable reflection at the interfaces of the phases.
An example are some glass fiber reinforced thermosets.

### Challenges on Practical Application

- Homogeneous lightning conditions
- Homogeneous specimen thickness
- Exploitation of complete range of light intensity of camera
- Identification of lower bound for neat resin (watch specimen thickness)
- Identification of local coordinate system

### Algorithm

- Identify linear mapping between local fiber volume fraction and light intensity
  from the following two measurements:
  	1. Light intensity in specific region with fiber volume fraction equals zero, i.e. without fibers
  	2. Average light intensity of specimen correlating with average volume fiber fraction of the specimen

Inverted light intensity, i.e. darkness:

```
     | --------------|----------------|---------------- |
 lower bound    neat resin     specimen mean       upper bound

```

![X-y plot of fiber volume fraction over grey value with two special point pairs: Average specimen and neat resin](doc/example_fiber_volume_fraction.png)

## Installation

- Clone the git-project to your machine
	```shell
	git clone 
	```
- Install the package from local repository into current environment in develop mode:
	```shell
	python setup.py develop
	```

Note: [Develop vs. install](https://stackoverflow.com/a/19048754/8935243)

## Usage

See [example script](fiberspot/example_script.py) generating
fields of volume fraction using different filter algorithms:

Original Image

![Image of fiber reinforced specimen with hair cross](data/specimen.png)

Gaussian filter with radius 60pixel

![Fiber volume fraction as colomap using box filter](doc/fvfs_gaussian_PIL.png)

Box mean with radius 60pixel

![Fiber volume fraction as colomap using box filter](doc/fvfs_box_PIL.png)

## Unpublished Features

Skimage mean filter using disk area with radius 60pixel and masked hair cross.

![Fiber volume fraction as colomap without hair cross visible in previous images](doc/fvfs_mean_disk_skimage_masked.png)
