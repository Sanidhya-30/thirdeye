import cv2
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from utils.utils import *
from matplotlib.widgets import Slider, Button

## ----- APPLY GAMMA CORRECTION ------ ##
def apply_gaco(image, gamma):

    f = lambda a : a ** gamma
 
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

    # Convert the modified HSV image back to BGR
    corrected_image_bgr = cv2.cvtColor(corrected_image, cv2.COLOR_HSV2RGB)

    return corrected_image_bgr
   

def main():
    
    global width,height 
    
    # Load image
    image_path = lena_path
    ogimage = cv2.imread(image_path)
    height,width, depth = ogimage.shape
    
    rgbimage = cv2.cvtColor(ogimage, cv2.COLOR_BGR2RGB)
    hsvimage = cv2.cvtColor(ogimage, cv2.COLOR_BGR2HSV)


    gamma = 0.5
    oimage = apply_gaco(hsvimage, gamma) 
    
    image_array = [(rgbimage, "Input"), (oimage, "Output")]
    Plot_Figure(image_array, rows=2, cols=1)   


if __name__ == "__main__":
    main()
