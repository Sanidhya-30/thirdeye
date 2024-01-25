import matplotlib.pyplot as plt
from PIL import Image
import cv2
from mpl_toolkits.mplot3d import Axes3D



def image_to_3d_array(image):
    """
    Convert a Pillow Image object to a 3D array.

    """
    print("converting image to array")
    return [[[pixel for pixel in row] for row in image.getdata()]]



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



def rgb2hsv(pixel): 
    r, g, b = pixel[0] / 255.0, pixel[1] / 255.0, pixel[2] / 255.0
    cmax, cmin = max(r, g, b), min(r, g, b)
    delta = cmax - cmin

    # Calculate hue
    if delta == 0:
        h = 0
    elif cmax == r:
        h = 60 * ((g - b) / delta % 6)
    elif cmax == g:
        h = 60 * ((b - r) / delta + 2)
    elif cmax == b:
        h = 60 * ((r - g) / delta + 4)

    # Calculate saturation
    s = 0 if cmax == 0 else delta / cmax

    # Calculate value
    v = cmax

    return int(h), int(s * 100), int(v * 100)



def rgb_to_hsv(rgb_image, width, height):
    print("converting rgb to hsv")
    hsv_image = Image.new("HSV", (width, height))
    for x in range(width):
        for y in range(height):
            pixel_rgb = rgb_image.getpixel((x, y))
            pixel_hsv = rgb2hsv(pixel_rgb)
            hsv_image.putpixel((x, y), pixel_hsv)
    return hsv_image


def main():
    # Load image
    image_path = "/home/ubuntu/thirdeye/src/task2/baboon.jpg"
    rgb_image = Image.open(image_path)
    print(rgb_image.size)
    width, height = rgb_image.size
    hsv_image = rgb_to_hsv(rgb_image, width, height)
    hsv_image.show()
    

if __name__ == "__main__":
    main()