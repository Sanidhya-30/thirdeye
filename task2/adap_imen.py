from PIL import Image
import math
import matplotlib.pyplot as plt
import cv2

## ----- FUNCTION TO PLOT MULTIPLE IMAGES TOGETHER ------ ##
def plot_images(*images):
    """
    Plot multiple images in a single figure.

    """
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



## ----- CONVERT IMAGE TO 3D ARRAY ------ ##
def image_to_3d_array(image):
    """
    Convert a Pillow Image object to a 3D array.

    """
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



## ----- CLASSIFY CONTRAST ------ ##
def checkcontrast(image):

    width, height = image.size

    # Initialize variables for mean and standard deviation calculation
    sum_value = 0
    sum_squared_diff = 0

    # Extract the value (brightness) channel and calculate sum of values
    for y in range(height):
        for x in range(width):
            h, s, v = image.getpixel((x, y))
            sum_value += v

    # Calculate mean value
    mean_value = sum_value / (width * height)

    # Calculate sum of squared differences for standard deviation
    for y in range(height):
        for x in range(width):
            h, s, v = image.getpixel((x, y))
            sum_squared_diff += (v - mean_value) ** 2

    # Calculate standard deviation
    std_dev_value = (sum_squared_diff / (width * height)) ** 0.5

    # Calculate the contrast measure D
    D = abs((mean_value + 2 * std_dev_value) - (mean_value - 2 * std_dev_value))

    return D, std_dev_value, mean_value


## ----- APPLY GAMMA CORRECTION ------ ##
def apply_gaco(image, mean_value, gamma):

    if mean_value >= 0.5:
        f = lambda a : a ** gamma
    else : 
        f = lambda a : (a ** gamma)/((a ** gamma) + (1-a ** gamma)*(mean_value**gamma))
    
    width, height = image.size

    # Create a new image with the same size and 'HSV' mode
    corrected_image = Image.new('HSV', (width, height))

    # Apply gamma correction pixel by pixel
    for y in range(height):
        for x in range(width):
            # Get the HSV values of the original pixel
            h, s, v = image.getpixel((x, y))
            v = v/255
            # Apply gamma correction to the value (brightness) channel
            v_corrected = int(255 * f(v))

            # Set the corrected pixel in the new image
            corrected_image.putpixel((x, y), (h, s, v_corrected))

    return corrected_image


## ----- ADAPTIVE IMAGE ENHANCEMENT FUNCTION ------ ##
def adap_imen(image, threshold=3):

    #check image HSV or RGB
    image = rgb_to_hsv(image)
    plot_images(image)

    D, sted_dev, mean_value = checkcontrast(image)

    #Check contrast high low
    if D < (1/threshold):
        gamma = -(math.log2(sted_dev))                  #high contrast
        oimage = apply_gaco(image, mean_value, gamma)    
    else:
        gamma = -math.exp((1-(mean_value+sted_dev))/2)                  #low contrast
        oimage = apply_gaco(image, mean_value, gamma)     

    oimage = hsv_to_rgb(oimage)
    # oimage = cv2.cvtColor(oimage, cv2.COLOR_HSV2RGB)
    return oimage
    

def main():
    # Load image
    image_path = "C://Users//sanid//OneDrive//Desktop//3rdiTech//task2//cat.jfif"
    original_image = Image.open(image_path)
    adimen_image = adap_imen(original_image)
    
    plot_images(original_image, adimen_image)   

if __name__ == "__main__":
    main()
