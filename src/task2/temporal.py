import cv2
import numpy as np

# Initialize video capture
cap = cv2.VideoCapture(0)

# Parameters for adaptive AGC
target_brightness = 120  # Adjust as needed
smooth_factor = 0.5  # Smoothing for temporal filtering
previous_gain = 1.0  # Initialize previous gain

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Calculate average brightness
    average_brightness = cv2.mean(gray)[0]

    # Calculate gain adjustment factor
    gain_factor = target_brightness / average_brightness
    # Combine with previous gain for temporal filtering
    current_gain = (smooth_factor * previous_gain + (1 - smooth_factor) * gain_factor)
    # Apply gain to frame
    adjusted_frame_float = frame.astype(float) * (current_gain)

    # Clip values to the valid range [0, 255]
    adjusted_frame = np.clip(adjusted_frame_float, 0, 255).astype(np.uint8)
    # Calculate gradients for detail-preserving AGC
    gradients = cv2.Laplacian(gray, cv2.CV_64F).var()

    r = gradients / 10000
    print(gradients.max())
    # Apply less gain in high-gradient areas (edges and textures)
    gain_map = 1 - abs(r)  # Normalize gradients
    gain_map = np.clip(gain_map, 0, 1)  # Clip values to [0, 1]
    gain_map = (gain_map * 255).astype(np.uint8)  # Convert to uint8 for multiplication

    # Apply gain map to each channel separately
    # for c in range(3):
    #     adjusted_frame[:, :, c] = np.multiply(adjusted_frame[:, :, c], gain_map)

    # Display the resulting frame
    cv2.imshow('Temporal AGC', adjusted_frame)
    cv2.imshow('OG', frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Update previous gain for the next frame
    previous_gain = current_gain

# Release resources
cap.release()
cv2.destroyAllWindows()
