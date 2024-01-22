import cv2
import numpy as np
import matplotlib.pyplot as plt
from ..utils import *


# Function to perform morphological operations on color image
def perform_morphological_operations(image):
    # Split the image into 3 channels (BGR)
    b, g, r = cv2.split(image)

    # Define a kernel for morphological operations
    kernel = np.ones((5, 5), np.uint8)

    # Function to perform morphological operations on a single channel
    def apply_morphology(channel):
        erosion = cv2.erode(channel, kernel, iterations=1)
        dilation = cv2.dilate(channel, kernel, iterations=1)
        opening = cv2.morphologyEx(channel, cv2.MORPH_OPEN, kernel)
        closing = cv2.morphologyEx(channel, cv2.MORPH_CLOSE, kernel)
        gradient = cv2.morphologyEx(channel, cv2.MORPH_GRADIENT, kernel)
        return erosion, dilation, opening, closing, gradient

    # Apply morphological operations on each channel
    b_erosion, b_dilation, b_opening, b_closing, b_gradient = apply_morphology(b)
    g_erosion, g_dilation, g_opening, g_closing, g_gradient = apply_morphology(g)
    r_erosion, r_dilation, r_opening, r_closing, r_gradient = apply_morphology(r)

    # Merge the channels back together
    output_erosion = cv2.merge((b_erosion, g_erosion, r_erosion))
    output_dilation = cv2.merge((b_dilation, g_dilation, r_dilation))
    output_opening = cv2.merge((b_opening, g_opening, r_opening))
    output_closing = cv2.merge((b_closing, g_closing, r_closing))
    output_gradient = cv2.merge((b_gradient, g_gradient, r_gradient))

    # Plot the results
    plot_images(image, output_erosion, output_dilation, output_opening, output_closing, output_gradient)

def main():
    # Read the input image
    image_path = "C://Users//sanid//OneDrive//Desktop//3rdiTech//task2//cat.jpg"
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)

    # Check if the image is loaded successfully
    if image is None:
        print("Error: Unable to load the image.")
        exit()  

    # Perform morphological operations and plot the results
    perform_morphological_operations(image)

if __name__ == "__main__":
    main()

