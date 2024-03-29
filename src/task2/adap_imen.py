from PIL import Image
import math
import cv2
from utils.utils import *


## ----- CLASSIFY CONTRAST ------ ##
def checkcontrast(image):
    
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

    # Calculate the contrast meqasure D
    D = abs((mean_value + 2 * std_dev_value) - (mean_value - 2 * std_dev_value))

    return D, std_dev_value, mean_value


## ----- APPLY GAMMA CORRECTION ------ ##
def apply_gaco(image, mean_value, gamma):

    if mean_value >= 0.5:
        f = lambda a : a ** gamma
    else : 
        f = lambda a : (a ** gamma)/((a ** gamma) + (1-a ** gamma)*(mean_value**gamma))
    
    # width, height = image.size

    # Create a new image with the same size and 'HSV' mode
    corrected_image = Image.new('HSV', (width, height))

    # Apply gamma correction pixel by pixel
    for y in range(height):
        for x in range(width):
            # Get the HSV values of the original pixel
            h, s, v = image.getpixel((x, y))
            v = v/255
            # Apply gamma correction to the value (brightness) channel
            if v != 0:
                v_corrected = int(255 * f(v))

            # Set the corrected pixel in the new image
            corrected_image.putpixel((x, y), (h, s, v_corrected))

    return corrected_image


## ----- ADAPTIVE IMAGE ENHANCEMENT FUNCTION ------ ##
def adap_imen(image_path, threshold=3):

    global width,height 

    image = Image.open(image_path)
    image = rgb_to_hsv(image)
    width, height = image.size

#cv2 methods    
    # image = cv2.imread(image_path)
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # height,width, depth = image.shape

    D, sted_dev, mean_value = checkcontrast(image)

    #Check contrast high low
    if D < (1/threshold):
        gamma = -(math.log2(sted_dev))                  #high contrast
        oimage = apply_gaco(image, mean_value, gamma)    
    else:
        gamma = -math.exp((1-(mean_value+sted_dev))/2)  #low contrast
        oimage = apply_gaco(image, mean_value, gamma)     

    oimage = hsv_to_rgb(oimage)
    # oimage = oimage.convert(mode="RGB")
    # oimage = cv2.cvtColor(oimage, cv2.COLOR_HSV2RGB)
    return oimage
    

def main():
    # Load image
    image_path = lena_path
    ogimage = Image.open(image_path)

    adimen_image = adap_imen(image_path)
    
    image_array = [(ogimage, "Input"), (adimen_image, "Output")]
    Plot_Figure(image_array, rows=2, cols=1)   

if __name__ == "__main__":
    main()
