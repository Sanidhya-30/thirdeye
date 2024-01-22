import matplotlib.pyplot as plt
from PIL import Image
import cv2


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



## ----- FUNCTION TO CONVERT HSV TO RGB ------ ##

def hsv2rgb(hsv_image):

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

def main():
    # Load image
    image_path = "/home/ubuntu/thirdeye/src/task2/cat_lowres.jpg"
    rgb_image = Image.open(image_path)
    hsv_image = hsv2rgb
    plot_images(rgb_image, hsv_image)   

if __name__ == "__main__":
    main()