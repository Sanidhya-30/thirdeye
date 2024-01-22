import cv2
import matplotlib.pyplot as plt
import numpy as np
from utils.utils import *

image = cv2.imread(cat_highres, cv2.IMREAD_GRAYSCALE)

if image is not None:

    # Perform histogram equalization
    equalized_image = cv2.equalizeHist(image)

    # Calculate histograms for the original and equalized images
    hist_original = cv2.calcHist([image], [0], None, [256], [0, 256])
    hist_equalized = cv2.calcHist([equalized_image], [0], None, [256], [0, 256])

    # Display the original and equalized images with their histograms
    plt.figure(figsize=(12, 8))

    # Plot original image
    plt.subplot(2, 2, 1)
    plt.imshow(image, cmap='gray')
    plt.title('Original Image')
    plt.axis('off')

    # Plot original histogram
    plt.subplot(2, 2, 2)
    plt.plot(hist_original, color='black')
    plt.title('Original Histogram')
    plt.xlabel('Pixel Intensity')
    plt.ylabel('Frequency')

    # Plot equalized image
    plt.subplot(2, 2, 3)
    plt.imshow(equalized_image, cmap='gray')
    plt.title('Equalized Image')
    plt.axis('off')

    # Plot equalized histogram
    plt.subplot(2, 2, 4)
    plt.plot(hist_equalized, color='black')
    plt.title('Equalized Histogram')
    plt.xlabel('Pixel Intensity')
    plt.ylabel('Frequency')

    plt.tight_layout()
    plt.show()
else:
    print("Error loading the image.")

