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
cat_medres = "/home/ubuntu/thirdeye/src/task2/cat.jfif"
creepy_path = "/home/ubuntu/thirdeye/src/task2/creepy.jpg"
lena_path = "/home/ubuntu/thirdeye/src/task2/lena.jpeg"

## ---------------------------------------------------- ##


## ----- CONVERT IMAGE TO 3D ARRAY ------ ##

def image_to_3d_array(image):
    return [list(pixel) for pixel in image.getdata()]



## ----- FUNCTION TO CONVERT RGB TO HSV ------ ##

def rgb_to_hsv(rgb_image):
    print("converting rgb to hsv")
    width, height = rgb_image.size
    hsv_image = Image.new('HSV', (width, height))
    # Iterate over each pixel in the HSV image
    for y in range(height):
        for x in range(width):
            r, g, b = rgb_image.getpixel((x, y))
            h,s,v = rgb2hsv(r,g,b)
            hsv_image.putpixel((x,y),(int(h),int(s),int(v)))
    return hsv_image




## ----- FUNCTION TO CONVERT HSV TO RGB ------ ##

def hsv_to_rgb(hsv_image):
        
    print("converting hsv to rgb")
    width, height = hsv_image.size
    rgb_image = Image.new('RGB', (width, height))
    # Iterate over each pixel in the HSV image
    for y in range(height):
        for x in range(width):
            h, s, v = hsv_image.getpixel((x, y))
            r ,g ,b = hsv2rgb(h,s,v)
            rgb_image.putpixel((x,y),(r,g,b))
    return rgb_image




## ----- FUNCTION TO CONVERT HSV TO RGB PIXEL-BY-PIXEL  ------ ##

def hsv2rgb(h, s, v):
    """
    Convert HSV (Hue, Saturation, Value) to RGB (Red, Green, Blue).

    """
    # Ensure the values are within the valid range for HSV
    h = h % 360
    s = max(0, min(s, 100))
    v = max(0, min(v, 100))

    # Convert HSV to RGB
    h /= 60.0
    s /= 100.0
    v /= 100.0

    hi = int(h) % 6
    f = h - int(h)
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)

    if hi == 0:
        return int(255 * v), int(255 * t), int(255 * p)
    elif hi == 1:
        return int(255 * q), int(255 * v), int(255 * p)
    elif hi == 2:
        return int(255 * p), int(255 * v), int(255 * t)
    elif hi == 3:
        return int(255 * p), int(255 * q), int(255 * v)
    elif hi == 4:
        return int(255 * t), int(255 * p), int(255 * v)
    else:  # hi == 5
        return int(255 * v), int(255 * p), int(255 * q)




## ----- FUNCTION TO CONVERT RGB TO HSV PIXEL-BY-PIXEL  ------ ##
    
def rgb2hsv(r, g, b): 
    r, g, b = r / 255.0, g / 255.0, b / 255.0
  
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
    return h,s,v




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

def Plot_Figure(images_with_titles, rows, cols):

    num_images = len(images_with_titles)

    # Create a new figure
    fig = plt.figure(figsize=(4 * cols, 4 * rows))

    for i in range(1, num_images+1):
        fig.add_subplot(rows, cols, i)
        plt.imshow(images_with_titles[i-1][0])
        plt.axis('off')  # Turn off axis labels
        plt.title(images_with_titles[i-1][1])

    plt.show()

def Plot_Image_and_Histogram(image_array):
    num_images = len(image_array)

    # Create a new figure with subplots
    fig, axs = plt.subplots(num_images, 2, figsize=(10, 5*num_images))

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
        axs[i, 1].plot(hist)
        axs[i, 1].set_title(f'Histogram - {title}')

    plt.show()
    

def keyboard_shutdown():
    print('Interrupted\n')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)

if __name__ == '__main__':
    pass