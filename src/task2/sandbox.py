from PIL import Image
import cv2
import matplotlib.pyplot as plt

def image_to_3d_array(image):
    return [list(pixel) for pixel in image.getdata()]

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

def conversion(image):
    width, height = image.size

    if image.mode == "RGB" :
        hsv_image = Image.new('HSV', (width, height))
        print("converting hsv to rgb")
        # Iterate over each pixel in the HSV image
        for y in range(height):
            for x in range(width):
                r, g, b = image.getpixel((x, y))
                h,s,v = rgb_to_hsv(r,g,b)
                hsv_image.putpixel((x,y),(int(h),int(s),int(v)))

        return hsv_image
    
    # elif image.mode == 'HSV' :
    else :
        rgb_image = Image.new('RGB', (width, height))
        print("converting hsv to rgb")

        # Iterate over each pixel in the HSV image
        for y in range(height):
            for x in range(width):
                h, s, v = image.getpixel((x, y))
                r ,g ,b = hsv_to_rgb(h,s,v)
                rgb_image.putpixel((x,y),(r,g,b))

        return rgb_image


def hsv_to_rgb(h, s, v):
    """
    Convert HSV (Hue, Saturation, Value) to RGB (Red, Green, Blue).

    """
    # Ensure the values are within the valid range for HSV
    h = h % 360
    s = max(0, min(s, 100))
    v = max(0, min(v, 100))

    # Convert HSV to RGB
    h /= 60.0
    s /= 100.0
    v /= 100.0

    hi = int(h) % 6
    f = h - int(h)
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)

    if hi == 0:
        return int(255 * v), int(255 * t), int(255 * p)
    elif hi == 1:
        return int(255 * q), int(255 * v), int(255 * p)
    elif hi == 2:
        return int(255 * p), int(255 * v), int(255 * t)
    elif hi == 3:
        return int(255 * p), int(255 * q), int(255 * v)
    elif hi == 4:
        return int(255 * t), int(255 * p), int(255 * v)
    else:  # hi == 5
        return int(255 * v), int(255 * p), int(255 * q)


def rgb_to_hsv(r, g, b): 
    r, g, b = r / 255.0, g / 255.0, b / 255.0
  
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
    return h,s,v


# Example usage:
image_path = "C://Users//sanid//OneDrive//Desktop//3rdiTech//task2//cat.jfif"
input_image_rgb = Image.open(image_path)
print(input_image_rgb.mode)

# Convert RGB to HSV using the function
output_image_hsv = conversion(input_image_rgb)
print(output_image_hsv.mode)
output_image_rgb = conversion(output_image_hsv)

im = cv2.imread(image_path)
hsv_img = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

plot_images(input_image_rgb, output_image_hsv, output_image_rgb)   

