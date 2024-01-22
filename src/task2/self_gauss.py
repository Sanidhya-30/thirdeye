from PIL import Image
import time
import cv2
from utils.utils import *

##Generate a 2D Gaussian kernel.
def gaussian_kernel(size, sigma=1.0):
    kernel = [[(1/(2 * cons_pi * sigma**2)) * cons_pi**(-((x - (size-1)/2)**2 + (y - (size-1)/2)**2) / (2 * sigma**2))
               for x in range(size)] for y in range(size)]
    normalization = sum(sum(row) for row in kernel)
    return [[value / normalization for value in row] for row in kernel]


# Apply Gaussian kernel tranversing over image
def apply_gaussian_smoothing(image, kernel_size=9, sigma=1.5):
    """
    Apply Gaussian smoothing to the image.

    """
    kernel = gaussian_kernel(kernel_size, sigma)
    image_width, image_height = len(image[0]), len(image)
    smoothed_image = [[0 for _ in range(image_width)] for _ in range(image_height)]
    kernel_center = kernel_size // 2
    for y in range(image_height):
        for x in range(image_width):
            weighted_sum = 0.0
            for ky in range(kernel_size):
                for kx in range(kernel_size):
                    img_x = min(max(0, x + kx - kernel_center), image_width - 1)
                    img_y = min(max(0, y + ky - kernel_center), image_height - 1)
                    # here min/max for edge cases, else coorinate = (y + ky - kernel_center)
                    weighted_sum += kernel[ky][kx] * image[img_y][img_x]
            smoothed_image[y][x] = int(weighted_sum)
    return smoothed_image


def gauss_bhai(image_path, kernel_size, sigma):
    start_time1 = time.time()   #start time    
    imageog = Image.open(image_path)
   
    if (len(imageog.split())) == 3:
        print("image is RGB")
        # convert 2 grey
        gray_image = rgb_to_gray(image_path)
   
    elif (len(imageog.split())) == 1:
        print("image is greyscale")
        gray_image=imageog

    # convert grey image to list
    image_data = list(gray_image.getdata())
    image_width, image_height = gray_image.size
    image_2d = [image_data[i:i + image_width] for i in range(0, len(image_data), image_width)]
    
    # Apply gaussian smoothening on grey image
    smoothed_image_2d = apply_gaussian_smoothing(image_2d, kernel_size, sigma)
    smoothed_image_data = [value for row in smoothed_image_2d for value in row]
    smoothed_image = Image.new("L", (image_width, image_height))
    smoothed_image.putdata(smoothed_image_data)
    
    end_time1 = time.time() # end time
    time_gauss = end_time1 - start_time1
    print("Time for self Gauss", time_gauss)
    
    return smoothed_image, time_gauss

def main():
    #define for gaussian blur
    kernel_size = 5  # Choose an odd number
    sigma = 1.5

    image_path = baboon_path
    imageog = Image.open(baboon_path)

    # apna gauss
    image1, timet = gauss_bhai(image_path, kernel_size, sigma)

    # opencv waalo ka gauss
    time1=time.time()
    image2 = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    image2 = cv2.GaussianBlur(image2, (kernel_size,kernel_size), sigma)
    time2=time.time()
    timeT = time2-time1
    print("Time for cv Gauss", timeT)
    plot_images(imageog, image1, image2)


if __name__ == "__main__":
    main()