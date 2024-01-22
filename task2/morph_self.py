import matplotlib.pyplot as plt
from PIL import Image

def rgb2gray(rgb_image):
    # Convert RGB to grayscale
    width, height = rgb_image.size
    gray_image = [[0 for _ in range(width)] for _ in range(height)]

    for y in range(height):
        for x in range(width):
            pixel = rgb_image.getpixel((x, y))
            gray_value = int(0.2989 * pixel[0] + 0.5870 * pixel[1] + 0.1140 * pixel[2])
            gray_image[y][x] = gray_value

    return gray_image

def add_salt_and_pepper_noise(image, salt_prob, pepper_prob):
    # Add salt-and-pepper noise to the input image
    width, height = len(image[0]), len(image)
    noisy_image = [row[:] for row in image]

    for y in range(height):
        for x in range(width):
            if (x * y) % 40 == 0:  # Salt noise
                noisy_image[y][x] = 255
            elif (x * y) % 43 == 0:  # Pepper noise
                noisy_image[y][x] = 0

    return noisy_image

def erosion(image, se):
    # Perform erosion on the input image
    width, height = len(image[0]), len(image)
    eroded_image = [[0 for _ in range(width)] for _ in range(height)]

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            min_value = min(image[y][x], image[y-1][x], image[y+1][x], image[y][x-1], image[y][x+1])
            eroded_image[y][x] = min_value

    return eroded_image

def dilation(image):
    # Perform dilation on the input image
    width, height = len(image[0]), len(image)
    dilated_image = [[0 for _ in range(width)] for _ in range(height)]

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            max_value = max(image[y][x], image[y-1][x], image[y+1][x], image[y][x-1], image[y][x+1])
            dilated_image[y][x] = max_value

    return dilated_image

def morphological_opening(image, se):
    # Perform morphological opening (erosion followed by dilation)
    eroded_image = erosion(image, se)
    opened_image = dilation(eroded_image, se)
    return opened_image

def morphological_closing(image, se):
    # Perform morphological closing (dilation followed by erosion)
    dilated_image = dilation(image)
    closed_image = erosion(dilated_image)
    return closed_image

# Read the image and convert it to grayscale
image_path = (r"C:\Users\VPS RATHORE\OneDrive\Desktop\3rdiTech\test.jpg")
rgb_image = Image.open(image_path).convert('RGB')
gray_image = rgb2gray(rgb_image)

# Add salt-and-pepper noise to the grayscale image
salt_prob = 0.05  # Adjust as needed
pepper_prob = 0.05  # Adjust as needed
noisy_image = add_salt_and_pepper_noise(gray_image, salt_prob, pepper_prob)

# Create a 3x3 structuring element of ones
se = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]

# Perform morphological opening
opened_image = morphological_opening(noisy_image, se)

# Perform morphological closing
closed_image = morphological_closing(opened_image, se)

# Display the results
plt.subplot(1, 4, 1)
plt.imshow(rgb_image)
plt.title('Original Image')

plt.subplot(1, 4, 2)
plt.imshow(gray_image, cmap='gray')
plt.title('Grayscale Image')

plt.subplot(1, 4, 3)
plt.imshow(noisy_image, cmap='gray')
plt.title('Noisy Image')

plt.subplot(1, 4, 4)
plt.imshow(closed_image, cmap='gray')
plt.title('Noise Removal Result')

plt.show()