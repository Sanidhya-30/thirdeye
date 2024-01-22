import cv2
import numpy as np
from utils.utils import *

def apply_mask(image, mask):
    # Ensure mask has the same number of channels as the image
    mask = mask[..., None] if image.ndim == 3 and mask.ndim == 2 else mask
    return image * (mask > 0)

def automatic_brightness_control(image, block_size=10, threshold=20, target_brightness=127):
    # Step 1: Local Brightness Analysis
    local_brightness = cv2.boxFilter(image, -1, (block_size, block_size))

    # Step 2: Calculate Local Brightness Deviation
    brightness_deviation = np.abs(local_brightness - target_brightness)

    # Step 3: Thresholding or Binarization
    mask = (brightness_deviation > threshold).astype(np.uint8) * 255

    # Step 4: Morphological Operations
    kernel = np.ones((block_size, block_size), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # Use closing operation

    # Step 5: Brightness Adjustment
    # Increase brightness by adding 30 and clip values to [0, 255]
    brightened_image = np.clip(image + 30, 0, 255).astype(np.uint8)

    # Apply the mask to limit the adjustment to regions where the mask is non-zero
    adjusted_image = apply_mask(brightened_image, mask)
    
    return brightened_image  # Ensure data type is uint8

# Example usage:
image = cv2.imread(cat_highres, cv2.IMREAD_GRAYSCALE)
# image = cv2.resize(image, (512,512))
if image is not None:
    adjusted_image = automatic_brightness_control(image)

    # Ensure the adjusted_image is in the correct data type (uint8)
    adjusted_image = adjusted_image.astype(np.uint8)

    # Convert to BGR if the image is grayscale
    if len(adjusted_image.shape) == 2:
        adjusted_image = cv2.cvtColor(adjusted_image, cv2.COLOR_GRAY2BGR)

    cv2.imshow('Original Image', image)
    cv2.imshow('Adjusted Image', adjusted_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Error loading the image.")