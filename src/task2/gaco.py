import cv2
import numpy as np
import matplotlib.pyplot as plt
from utils.utils import *  
from matplotlib.widgets import Slider, Button

def Plot_Image_and_Histogram(image_array, fig, axs):
    num_images = len(image_array)

    for i in range(num_images):
        image = image_array[i][0]
        title = image_array[i][1]

        # Plot the image on the left subplot
        axs[i, 0].imshow(image)
        axs[i, 0].axis('off')  # Turn off axis labels
        axs[i, 0].set_title(f'Image - {title}')

        # Plot the histogram on the right subplot
        if len(image.shape) == 3:
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray_image = image
        hist = cv2.calcHist([gray_image], [0], None, [256], [0, 256])
        axs[i, 1].cla()  # Clear existing histogram
        axs[i, 1].plot(hist)
        axs[i, 1].set_title(f'Histogram - {title}')

    fig.canvas.draw_idle()


def apply_gaco_rgb(image, gamma):
    normalized_image = image / 255.0
    corrected_image = np.power(normalized_image, gamma)
    corrected_image = np.clip(corrected_image, 0, 1)
    corrected_image *= 255
    corrected_image = corrected_image.astype(np.uint8)    
    return corrected_image

def apply_gaco_hsv(image, gamma):
    v_channel = image[:, :, 2] / 255.0
    v_corrected = (np.power(v_channel, gamma) * 255).astype(np.uint8)
    image[:, :, 2] = v_corrected
    corrected_image_rgb = cv2.cvtColor(image, cv2.COLOR_HSV2RGB)
    return corrected_image_rgb

def update_gamma(val):
    global gamma
    gamma = slider.val
    hsvoutim = apply_gaco_hsv(hsvimage.copy(), gamma)
    rgboutim = apply_gaco_rgb(rgbimage.copy(), gamma)
    image_array = [(rgbimage, "Input"), (rgboutim, "RGB Gaco"),(hsvoutim, "HSV GaCo")]
    Plot_Image_and_Histogram(image_array, fig, axs)

if __name__ == "__main__":
    global width, height

    # Load image
    image_path = lena_path
    ogimage = cv2.imread(image_path)
    height, width, depth = ogimage.shape

    rgbimage = cv2.cvtColor(ogimage, cv2.COLOR_BGR2RGB)
    hsvimage = cv2.cvtColor(ogimage, cv2.COLOR_BGR2HSV)

    gamma = 0.5

    fig, axs = plt.subplots(3, 2, figsize=(10, 10))
    plt.subplots_adjust(bottom=0.25)

    slider_ax = plt.axes([0.2, 0.01, 0.65, 0.03])
    slider = Slider(slider_ax, 'Gamma', 0.1, 5.0, valinit=gamma)
    slider.on_changed(update_gamma)

    hsvoutim = apply_gaco_hsv(hsvimage.copy(), gamma)
    rgboutim = apply_gaco_rgb(rgbimage.copy(), gamma)
    image_array = [(rgbimage, "Input"), (rgboutim, "RGB Gaco"),(hsvoutim, "HSV GaCo")]
    Plot_Image_and_Histogram(image_array, fig, axs)

    plt.show()
