from PIL import Image
import math
from utils.utils import *

def fourier_transform(image):
    width, height = image.size
    img_data = image.getdata()
    
    result_real = [[0.0] * width for _ in range(height)]
    result_imag = [[0.0] * width for _ in range(height)]

    for v in range(height):
        for u in range(width):
            sum_real = 0.0
            sum_imag = 0.0

            for y in range(height):
                for x in range(width):
                    pixel_value = img_data[y * width + x]
                    angle = 2 * math.pi * ((u * x / width) + (v * y / height))
                    sum_real += pixel_value * math.cos(angle)
                    sum_imag -= pixel_value * math.sin(angle)

            result_real[v][u] = sum_real / width / height
            result_imag[v][u] = sum_imag / width / height

    return result_real, result_imag

def inverse_fourier_transform(real_part, imag_part):
    height = len(real_part)
    width = len(real_part[0])

    result = Image.new("L", (width, height))

    for y in range(height):
        for x in range(width):
            sum_value = 0.0

            for v in range(height):
                for u in range(width):
                    angle = 2 * math.pi * ((u * x / width) + (v * y / height))
                    sum_value += (real_part[v][u] * math.cos(angle) - imag_part[v][u] * math.sin(angle))

            pixel_value = int(sum_value + 0.5)
            result.putpixel((x, y), pixel_value)

    return result

def remove_high_frequency(real_part, imag_part, threshold):
    height = len(real_part)
    width = len(real_part[0])

    for v in range(height):
        for u in range(width):
            magnitude = math.sqrt(real_part[v][u] ** 2 + imag_part[v][u] ** 2)
            if magnitude > threshold:
                real_part[v][u] = 0.0
                imag_part[v][u] = 0.0

def main():
    # Load image
    image_path = cat_lowres
    original_image = Image.open(image_path).convert("L")

    # Fourier Transform
    real_part, imag_part = fourier_transform(original_image)

    # Remove high frequencies (noise)
    threshold = 100.0  # Adjust as needed
    remove_high_frequency(real_part, imag_part, threshold)

    # Inverse Fourier Transform
    reconstructed_image = inverse_fourier_transform(real_part, imag_part)

    # Display original and reconstructed images
    original_image.show(title="Original Image")
    reconstructed_image.show(title="Reconstructed Image")

if __name__ == "__main__":
    main()
