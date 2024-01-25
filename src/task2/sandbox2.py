import cv2
import matplotlib.pyplot as plt
import numpy as np
from utils.utils import *


## ----- CLASSIFY CONTRAST ------ ##
def checkcontrast(image):
    
    # Initialize variables for mean and standard deviation calculation
    sum_value = 0
    sum_squared_diff = 0

    # Extract the value (brightness) channel and calculate sum of values
    for y in range(width):
        for x in range(height):
            (h, s, v) = image[x, y]
            sum_value += v

    # Calculate mean value
    mean_value = sum_value / (width * height)

    # Calculate sum of squared differences for standard deviation
    for y in range(width):
        for x in range(height):
            h, s, v = image[x, y]
            sum_squared_diff += (v - mean_value) ** 2

    # Calculate standard deviation
    std_dev_value = (sum_squared_diff / (width * height)) ** 0.5

    # Calculate the contrast measure D
    D = abs((mean_value + 2 * std_dev_value) - (mean_value - 2 * std_dev_value))

    # cv2.imshow("check contrast", image)
    # cv2.waitKey(0) 

    return D, std_dev_value, mean_value


## ----- APPLY GAMMA CORRECTION ------ ##
def apply_gaco(image, mean_value, gamma):

    if mean_value >= 0.5:
        f = lambda a : a ** gamma
    else : 
        f = lambda a : (a ** gamma)/((a ** gamma) + (1-a ** gamma)*(mean_value**gamma))
    
    corrected_image = image

    # Apply gamma correction pixel by pixel
    for y in range(width):
        for x in range(height):
            # Get the HSV values of the original pixel
            (h, s, v) = image[x, y]
            v = v/255
            # Apply gamma correction to the value (brightness) channel
            if v != 0:
                v_corrected = int(255 * f(v))

            # Set the corrected pixel in the new image
            corrected_image[x, y] = (h, s, v_corrected)

    # cv2.imshow("apply gaco", corrected_image)
    # cv2.waitKey(0) 

    return corrected_image


## ----- ADAPTIVE IMAGE ENHANCEMENT FUNCTION ------ ##
def adap_imen(image, threshold=3):

    global width,height 
    height,width, depth = image.shape

    D, sted_dev, mean_value = checkcontrast(image)

    #Check contrast high low
    if D < (1/threshold):
        gamma = -(np.log2(sted_dev))                  #high contrast
        oimage = apply_gaco(image, mean_value, gamma)    
    else:
        gamma = -np.exp((1-(mean_value+sted_dev))/2)  #low contrast
        oimage = apply_gaco(image, mean_value, gamma)     

    print(oimage)
    oimage = cv2.cvtColor(oimage, cv2.COLOR_HSV2RGB)

    return oimage
    

def main():
    # Load image
    image_path = cat_medres
    ogimage = cv2.imread(image_path)
    hsvimage = cv2.cvtColor(ogimage, cv2.COLOR_BGR2HSV)
    adimen_image = adap_imen(hsvimage)    
    image_array = [(ogimage, "Input"), (adimen_image, "Output")]
    Plot_Figure(image_array, rows=2, cols=1)   


if __name__ == "__main__":
    main()
