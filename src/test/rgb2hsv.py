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


def rgb2hsv(rgb_image):
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

def main():
    # Load image
    image_path = "/home/ubuntu/thirdeye/src/task2/cat_lowres.jpg"
    rgb_image = Image.open(image_path)
    hsv_image = rgb2hsv(rgb_image)
    
    plot_images(rgb_image, hsv_image)   

if __name__ == "__main__":
    main()