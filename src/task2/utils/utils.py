import sys
import os
import matplotlib.pyplot as plt
from PIL import Image
import cv2 


## ----- DEFINING CONSTANTS ------ ##

cons_pi = 3.14159265
cons_e = 2.71828
baboon_path = "/home/ubuntu/thirdeye/src/task2/baboon.jpg"
cat_grey = "/home/ubuntu/thirdeye/src/task2/cat_grey.jfif"
cat_lowres = "/home/ubuntu/thirdeye/src/task2/cat_lowres.jpg"
cat_highres = "/home/ubuntu/thirdeye/src/task2/cat.jpg"
cat_medres = "/home/ubuntu/thirdeye/src/task2/cat.jpg"
creepy = "/home/ubuntu/thirdeye/src/task2/creepy.jpg"


## ----- CONVERT IMAGE TO 3D ARRAY ------ ##

def image_to_3d_array(image):
    """
    Convert a Pillow Image object to a 3D array.

    """
    print("converting image to array")

    width, height = image.size
    array_3d = []

    for y in range(height):
        row = []
        for x in range(width):
            pixel = image.getpixel((x, y))
            row.append(pixel)
        array_3d.append(row)

    return array_3d



## ----- FUNCTION TO CONVERT RGB TO HSV ------ ##

def rgb_to_hsv(rgb_image):
    print("converting rgb to hsv")
    rgb_array = image_to_3d_array(rgb_image)
    height, width, _ = len(rgb_array), len(rgb_array[0]), len(rgb_array[0][0])
    hsv_array = [[[0.0, 0.0, 0.0] for _ in range(width)] for _ in range(height)]

    for y in range(height):
        for x in range(width):
            r, g, b = rgb_array[y][x]

            # Normalize RGB values to the range [0, 1]
            r, g, b = r / 255.0, g / 255.0, b / 255.0

            # h, s, v = hue, saturation, value 
            cmax = max(r, g, b)    # maximum of r, g, b 
            cmin = min(r, g, b)    # minimum of r, g, b 
            diff = cmax-cmin       # diff of cmax and cmin. 
        
            # if cmax and cmax are equal then h = 0 
            if cmax == cmin:  
                h = 0
            
            # if cmax equal r then compute h 
            elif cmax == r:  
                h = (60 * ((g - b) / diff) + 360) % 360
        
            # if cmax equal g then compute h 
            elif cmax == g: 
                h = (60 * ((b - r) / diff) + 120) % 360
        
            # if cmax equal b then compute h 
            elif cmax == b: 
                h = (60 * ((r - g) / diff) + 240) % 360
        
            # if cmax equal zero 
            if cmax == 0: 
                s = 0
            else: 
                s = (diff / cmax) * 100
        
            # compute v 
            v = cmax * 100

            hsv_array[y][x] = [h, s, v]

    print(len(hsv_array[0][0]))
    hsv_image = Image.new("HSV", rgb_image.size)
    hsv_image.putdata([(int(pixel[0] * 360), int(pixel[1] * 255), int(pixel[2] * 255)) for row in hsv_array for pixel in row])
    
    return hsv_image


## ----- FUNCTION TO CONVERT HSV TO RGB ------ ##

def hsv_to_rgb(hsv_image):
    print("converting hsv to rgb")
    # Get the size of the image
    width, height = hsv_image.size

    # Create a new image with the same size and 'RGB' mode
    rgb_image = Image.new('RGB', (width, height))

    # Iterate over each pixel in the HSV image
    for y in range(height):
        for x in range(width):
            # Get HSV values of the original pixel
            h, s, v = hsv_image.getpixel((x, y))

            # Perform the HSV to RGB conversion using mathematical operations
            C = v * s
            X = C * (1 - abs((h / 60) % 2 - 1))
            m = v - C

            if 0 <= h < 60:
                r, g, b = (C, X, 0)
            elif 60 <= h < 120:
                r, g, b = (X, C, 0)
            elif 120 <= h < 180:
                r, g, b = (0, C, X)
            elif 180 <= h < 240:
                r, g, b = (0, X, C)
            elif 240 <= h < 300:
                r, g, b = (X, 0, C)
            else:
                r, g, b = (C, 0, X)

            # Adjust RGB values and convert to integers in the range [0, 255]
            R, G, B = [int((x + m) * 255) for x in (r, g, b)]

            # Set the RGB pixel in the new image
            rgb_image.putpixel((x, y), (R, G, B))

    return rgb_image



## ----- FUNCTION TO CONVERT RGB TO GREY ------ ##

def rgb_to_gray(rgb_image):
    print("converting rgb to gray")
    # Convert RGB to grayscale
    width, height = rgb_image.size
    gray_image = [[0 for _ in range(width)] for _ in range(height)]

    for y in range(height):
        for x in range(width):
            pixel = rgb_image.getpixel((x, y))
            gray_value = int(0.2989 * pixel[0] + 0.5870 * pixel[1] + 0.1140 * pixel[2])
            gray_image[y][x] = gray_value

    return gray_image




## ----- PLOT IMAGES IN SAME FIGURE ------ ##

def plot_images(*images):
    """
    Plot multiple images in a single figure.

    """
    print("plotting")
    num_images = len(images)
    rows = 1
    cols = num_images

    # Create a new figure
    fig, axes = plt.subplots(rows, cols, figsize=(4 * cols, 4))

    # If only one image is provided, axes is a single Axes object, not an array
    if num_images == 1:
        axes = [axes]

    for i, ax in enumerate(axes):
        ax.imshow(images[i])
        ax.axis('off')  # Turn off axis labels

    plt.show()


def keyboard_shutdown():
    print('Interrupted\n')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)

if __name__ == '__main__':
    pass