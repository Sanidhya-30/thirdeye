import cv2
import numpy as np
import pywt
from utils.utils import *

# Normal methods
def digital_zoom(image, zoom_factor, interpolation_method=cv2.INTER_NEAREST):
    # Get original image dimensions
    height, width = image.shape[:2]

    # Calculate new dimensions based on zoom factor
    new_width = int(width * zoom_factor)
    new_height = int(height * zoom_factor)

    # Resize the image using the specified interpolation method
    zoomed_image = cv2.resize(image, (new_width, new_height), interpolation=interpolation_method)

    return zoomed_image

##  Wavelet methods ##
def wavelet_zoom(image, wavelet_basis='db4', decomposition_level=2, zoom_factor=2):
    #convert image for pywt lib to use
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = np.float32(image)
    image /= 255

    # DWT --> interpolate --> IDWT
    coeffs = pywt.wavedec2(image, wavelet=wavelet_basis, level=decomposition_level)
    print (coeffs)
    coeffs = np.array(coeffs)
    coeff_im = cv2.imread(image, 0)
    resized_coeffs = []
    for c in coeffs:
        resized_c = cv2.resize(coeff_im, None, fx=zoom_factor, fy=zoom_factor, interpolation=cv2.INTER_CUBIC)
        resized_coeffs.append(resized_c)
    zoomed_image = pywt.waverec2(resized_coeffs, wavelet=wavelet_basis)
    
    #convert image for opencv lib to use
    zoomed_image *= 255
    zoomed_image = np.uint8(zoomed_image)
    return zoomed_image

# Lanczos methods
def lanczos_zoom(image, zoom_factor, lanczos_window=3):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Define Lanczos filter
    def lanczos(x):
        s = np.sin(np.pi * x) / (np.pi * x)
        if lanczos_window > 0:
            w = np.sin(np.pi * x / lanczos_window) / (np.pi * x / lanczos_window)
            w[abs(x) >= lanczos_window] = 0
            return s * w
        else:
            return s
    # Apply FFT, filter, and inverse FFT
    dft = cv2.dft(np.float32(image), flags=cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)
    rows, cols = image.shape
    crow, ccol = rows // 2, cols // 2
    # mask = np.zeros((rows, cols, 2), np.uint8)
    # mask[int(crow-zoom_factor*crow:crow+zoom_factor*crow), int(ccol-zoom_factor*ccol:ccol+zoom_factor*ccol)] = 1
    fshift = dft_shift * lanczos(np.linspace(-0.5, 0.5, cols)[np.newaxis]) * lanczos(np.linspace(-0.5, 0.5, rows)[:, np.newaxis])
    ishift = np.fft.ifftshift(fshift)
    idft = cv2.idft(ishift)
    zoomed_image = cv2.magnitude(idft[:, :, 0], idft[:, :, 1])
    return zoomed_image

# Edge Directed
def edge_directed_zoom(image, zoom_factor, interpolation_method=cv2.INTER_LINEAR):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(image, 50, 150) 
    weights = cv2.distanceTransform(edges, distanceType=cv2.DIST_L2, maskSize=5)
    zoomed_image = cv2.resize(image, None, fx=zoom_factor, fy=zoom_factor, interpolation=interpolation_method)
    z = cv2.resize(image, None, fx = zoom_factor, fy=zoom_factor, interpolation = interpolation_method)
    return zoomed_image


## Main Code 
image = cv2.imread(creepy) # Load an image
zoom_factor = 3.0  # Adjust Zoom Factor as needed

nearest_zoomed = digital_zoom(image, zoom_factor, interpolation_method=cv2.INTER_NEAREST)
bilinear_zoomed = digital_zoom(image, zoom_factor, interpolation_method=cv2.INTER_LINEAR)
bicubic_zoomed = digital_zoom(image, zoom_factor, interpolation_method=cv2.INTER_CUBIC)
lanczos_zoomed = digital_zoom(image, zoom_factor, interpolation_method=cv2.INTER_LANCZOS4)
# wavelet_zoomed = wavelet_zoom(image, wavelet_basis='db4', decomposition_level=2, zoom_factor=2)
edge_directed_zoomed = edge_directed_zoom(image, zoom_factor)

# Display the combined images
# im_arr = [(image, "input"), (nearest_zoomed, "nearest naighbour"), (bilinear_zoomed, "Bilinear"), (bicubic_zoomed, "Bicubic"), (wavelet_zoomed, "Wavelet"),(edge_directed_zoomed, "edge directed")]
# Plot_Figure(im_arr, rows=2, cols=3)
plot_images(image, nearest_zoomed, bilinear_zoomed, bicubic_zoomed, lanczos_zoomed)

cv2.waitKey(0)
cv2.destroyAllWindows()
