import os
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import numpy as np

# Bands: R, G, B, alpha
# Modes: RGB, L


directory = os.path.join("plots", "002")
os.makedirs(directory, exist_ok=True)

path = os.path.realpath(os.path.join("data", "knips_04", "SpecimenAndPureresin.JPG"))
image = Image.open(path)

regions = {
    "specimen": {"box": (1340, 360, 2700, 1700)},
    "neat_resin": {"box": (3230, 2220, 4650, 3550)},
}

for key_region, region in regions.items():

    original = image.crop(region["box"])

    # plt.imshow(specimen)

    red, green, blue = original.split()
    luminance = original.copy().convert("L")

    inverted = ImageOps.invert(luminance)
    array = np.array(inverted)

    ########################################
    # Plot bands
    # Conclusion: Use luminance

    if True:
        aspect_ratio = array.shape[0] / array.shape[1]
        fig, axs = plt.subplots(3, 2, figsize=(2 * 6, 3 * 6 * aspect_ratio))
        subplots = {
            "RGB": {"image": original, "ax": axs[0, 0]},
            "Red": {"image": red, "ax": axs[0, 1]},
            "Green": {"image": green, "ax": axs[1, 0]},
            "Blue": {"image": blue, "ax": axs[1, 1]},
            "Luminance": {"image": luminance, "ax": axs[2, 0]},
            "Inverted luminance": {"image": inverted, "ax": axs[2, 1]},
        }

        for key_sub, data_sub in subplots.items():
            ax = data_sub["ax"]
            ax.imshow(data_sub["image"])
            ax.set_title(key_sub)

        path_picture = os.path.join(directory, f"modes_{key_region}")
        plt.savefig(path_picture + ".png")
        plt.tight_layout()
        plt.close(fig)

    ########################################
    # Plot histograms of bands

    if True:
        aspect_ratio = array.shape[0] / array.shape[1]
        fig, axs = plt.subplots(3, 2, figsize=(2 * 6, 3 * 6 * aspect_ratio))
        subplots = {
            "Red": {"image": red, "ax": axs[0, 1]},
            "Green": {"image": green, "ax": axs[1, 0]},
            "Blue": {"image": blue, "ax": axs[1, 1]},
            "Luminance": {"image": luminance, "ax": axs[2, 0]},
            "Inverted luminance": {"image": inverted, "ax": axs[2, 1]},
        }

        for key_sub, data_sub in subplots.items():
            ax = data_sub["ax"]
            data = np.array(data_sub["image"]).flatten()
            b, bins, patches = ax.hist(data, 255)
            ax.set_xlim(0, 255)
            ax.set_title(key_sub)

        path_picture = os.path.join(directory, f"modes_histograms_{key_region}")
        plt.savefig(path_picture + ".png")
        plt.tight_layout()
        plt.close(fig)
