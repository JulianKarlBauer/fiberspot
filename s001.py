import os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate

# Bands: R G B alpha
# Modes: RGB, L


directory = os.path.join("plots", "001")
os.makedirs(directory, exist_ok=True)

name_image = "IMG_9380.JPG"
path = os.path.realpath(os.path.join("data", name_image))
image = Image.open(path)

box = (300, 200, 900, 500)
region = image.crop(box)

region.save(
    os.path.splitext(os.path.realpath(os.path.join("output", name_image)))[0] + ".tiff"
)
red, green, blue = region.split()
luminance = region.copy().convert("L")

array = np.array(luminance)

########################################
# Plot bands
# Conclusion: Use luminance

if False:
    aspect_ratio = array.shape[0] / array.shape[1]
    fig, axs = plt.subplots(2, 2, figsize=(18, 18 * aspect_ratio))
    subplots = {
        "Red": {"image": red, "ax": axs[0, 0]},
        "Green": {"image": green, "ax": axs[0, 1]},
        "Blue": {"image": blue, "ax": axs[1, 0]},
        "Luminance": {"image": luminance, "ax": axs[1, 1]},
    }

    for key_sub, data_sub in subplots.items():
        ax = data_sub["ax"]
        ax.imshow(data_sub["image"])
        ax.set_title(key_sub)

    path_picture = os.path.join(directory, f"modes")
    plt.savefig(path_picture + ".png")
    plt.tight_layout()
    plt.close(fig)

########################################
# Mesh
n_x, n_y = 10, 10
l_y, l_x = array.shape
start_x, start_y = l_x / (2.0 * n_x), l_y / (2.0 * n_y)
end_x, end_y = l_x - start_x, l_y - start_y
x = np.linspace(start_x, end_x, n_x)
y = np.linspace(start_y, end_y, n_y)
xx, yy = np.meshgrid(x, y)

########################################
# Plot grid
if True:
    plt.figure()
    plt.imshow(array)
    plt.scatter(xx, yy, marker="x", c="k")
    plt.title("Grid points")

    path_picture = os.path.join(directory, f"grid")
    plt.savefig(path_picture + ".png")
    plt.tight_layout()

########################################
# Local fiber volume content


class LocalFiberVolumeContent:
    def __init__(
        self, average_value, average_volume_content, neat_value, neat_volume_content=0,
    ):
        self.average_value = average_value
        self.average_volume_content = average_volume_content
        self.neat_value = neat_value
        self.neat_volume_content = neat_volume_content
        x = [neat_value, average_value]
        y = [neat_volume_content, average_volume_content]
        self.interpolation = scipy.interpolate.interp1d(x, y, fill_value="extrapolate")

    def __call__(self, value):
        return self.interpolation(value)


fvc_map = LocalFiberVolumeContent(
    average_value=np.mean(array), average_volume_content=0.27, neat_value=0
)

if True:
    plt.figure()
    x = np.linspace(0, 256, 300)
    y = fvc_map(value=x)
    plt.plot(x, y)
    plt.xlabel("Grey value")
    plt.ylabel("Fiber volume content")
    plt.title("Get fiber volume content from grey value")

    path_picture = os.path.join(directory, f"fvc")
    plt.savefig(path_picture + ".png")
    plt.tight_layout()
