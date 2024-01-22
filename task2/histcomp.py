import cv2
import matplotlib.pyplot as plt

def load_image(image_path):
    # Load the image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    return image

def plot_image_and_histogram(axs, image, title):
    # Plot the image
    axs[0].imshow(image, cmap='gray')
    axs[0].set_title(title)
    axs[0].axis('off')

    # Plot the histogram
    axs[1].hist(image.flatten(), bins=256, range=[0, 256], color='gray', alpha=0.7)
    axs[1].set_title('Histogram')
    axs[1].set_xlim([0, 256])

def local_histogram_equalization(image, kernel_size=(3, 3)):
    # Apply Local Histogram Equalization (LHE)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=kernel_size)
    equalized_image = clahe.apply(image)
    return equalized_image

def global_histogram_equalization(image):
    # Apply Global Histogram Equalization (GHE)
    equalized_image = cv2.equalizeHist(image)
    return equalized_image

def adaptive_histogram_equalization(image, clip_limit=2.0, grid_size=(8, 8)):
    # Apply Adaptive Histogram Equalization (AHE)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=grid_size)
    equalized_image = clahe.apply(image)
    return equalized_image

def contrast_limited_adaptive_histogram_equalization(image, clip_limit=2.0, grid_size=(8, 8)):
    # Apply Contrast Limited Adaptive Histogram Equalization (CLAHE)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=grid_size)
    equalized_image = clahe.apply(image)
    return equalized_image

# Example usage:
image_path = 'C://Users//sanid//OneDrive//Desktop//3rdiTech//task2//cat.jfif'
original_image = load_image(image_path)

# Apply image processing methods
lhe_image = local_histogram_equalization(original_image)
ghe_image = global_histogram_equalization(original_image)
ahe_image = adaptive_histogram_equalization(original_image)
clahe_image = contrast_limited_adaptive_histogram_equalization(original_image)

# Plot images and histograms side by side
fig, axs = plt.subplots(5, 2, figsize=(12, 16))

# Original Image and Histogram
plot_image_and_histogram(axs[0, :], original_image, 'Original Image')

# Local Histogram Equalization (LHE)
plot_image_and_histogram(axs[1, :], lhe_image, 'Local Histogram Equalization (LHE)')

# Global Histogram Equalization (GHE)
plot_image_and_histogram(axs[2, :], ghe_image, 'Global Histogram Equalization (GHE)')

# Adaptive Histogram Equalization (AHE)
plot_image_and_histogram(axs[3, :], ahe_image, 'Adaptive Histogram Equalization (AHE)')

# Contrast Limited Adaptive Histogram Equalization (CLAHE)
plot_image_and_histogram(axs[4, :], clahe_image, 'Contrast Limited Adaptive Histogram Equalization (CLAHE)')

plt.tight_layout()
plt.show()
