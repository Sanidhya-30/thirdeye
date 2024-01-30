import cv2
import numpy as np
import matplotlib.pyplot as plt
from utils.utils import *
from matplotlib.widgets import Slider, Button

def apply_gaco(image, gamma):

    v_channel = image[:, :, 2] / 255.0
    v_corrected = (np.power(v_channel, gamma) * 255).astype(np.uint8)
    image[:, :, 2] = v_corrected
    corrected_image_rgb = cv2.cvtColor(image, cv2.COLOR_HSV2RGB)

    return corrected_image_rgb

def main():
    global width, height

    # Load image
    image_path = lena_path
    ogimage = cv2.imread(image_path)
    height, width, depth = ogimage.shape

    rgbimage = cv2.cvtColor(ogimage, cv2.COLOR_BGR2RGB)
    hsvimage = cv2.cvtColor(ogimage, cv2.COLOR_BGR2HSV)

    gamma = 0.5
    oimage = apply_gaco(hsvimage.copy(), gamma)  # Copy to avoid modifying the original image in-place

    image_array = [(rgbimage, "Input"), (oimage, "Output")]
    Plot_Image_and_Histogram(image_array)

if __name__ == "__main__":
    main()
