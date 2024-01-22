import matplotlib.pyplot as plt
from PIL import Image
from ..utils import *

def erosion(image, se):
    # Perform erosion on the input image
    width, height = len(image[0]), len(image)
    eroded_image = [[0 for _ in range(width)] for _ in range(height)]

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            min_value = min(image[y][x], image[y-1][x], image[y+1][x], image[y][x-1], image[y][x+1])
            eroded_image[y][x] = min_value

    return eroded_image

def dilation(image):
    # Perform dilation on the input image
    width, height = len(image[0]), len(image)
    dilated_image = [[0 for _ in range(width)] for _ in range(height)]

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            max_value = max(image[y][x], image[y-1][x], image[y+1][x], image[y][x-1], image[y][x+1])
            dilated_image[y][x] = max_value

    return dilated_image

def morphological_opening(image, se):
    # Perform morphological opening (erosion followed by dilation)
    eroded_image = erosion(image, se)
    opened_image = dilation(eroded_image, se)
    return opened_image

def morphological_closing(image, se):
    # Perform morphological closing (dilation followed by erosion)
    dilated_image = dilation(image)
    closed_image = erosion(dilated_image)
    return closed_image


def main():
        # Read the image and convert it to grayscale
    image_path = "C://Users//sanid//OneDrive//Desktop//3rdiTech//task2//cat.jfif"
    rgb_image = Image.open(image_path).convert('RGB')
    gray_image = rgb_to_gray(rgb_image)

    # Create a 3x3 structuring element of ones
    se = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]

    # Perform morphological opening
    opened_image = morphological_opening(gray_image, se)

    # Perform morphological closing
    closed_image = morphological_closing(opened_image, se)
        
    plot_images(gray_image, opened_image, closed_image)   

if __name__ == "__main__":
    main()