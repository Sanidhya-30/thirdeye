import cv2
from ..utils import *


def local_histogram_equalization(image, kernel_size=(3, 3)):
    # Apply Local Histogram Equalization (LHE)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=kernel_size)
    equalized_image = clahe.apply(image)
    return equalized_image

def global_histogram_equalization(image):
    # Apply Global Histogram Equalization (GHE)
    equalized_image = cv2.equalizeHist(image)
    return equalized_image

def adaptive_histogram_equalization(image, clip_limit=2.0, grid_size=(8, 8)):
    # Apply Adaptive Histogram Equalization (AHE)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=grid_size)
    equalized_image = clahe.apply(image)
    return equalized_image

def contrast_limited_adaptive_histogram_equalization(image, clip_limit=2.0, grid_size=(8, 8)):
    # Apply Contrast Limited Adaptive Histogram Equalization (CLAHE)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=grid_size)
    equalized_image = clahe.apply(image)
    return equalized_image


def main():
    # Example usage:
    image_path = 'C://Users//sanid//OneDrive//Desktop//3rdiTech//task2//cat.jfif'
    original_image = Image.open(image_path)

    # Apply image processing methods
    lhe_image = local_histogram_equalization(original_image)
    ghe_image = global_histogram_equalization(original_image)
    ahe_image = adaptive_histogram_equalization(original_image)
    clahe_image = contrast_limited_adaptive_histogram_equalization(original_image)

    plot_images(lhe_image, ghe_image, ahe_image, clahe_image)   

if __name__ == "__main__":
    main()