import cv2

# Initialize video capture object
cap = cv2.VideoCapture(0)  # Adjust index if multiple cameras

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # frame = cv2.imread("test.jpg")
    # Convert frame to grayscale for simplicity
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Calculate average brightness
    average_brightness = cv2.mean(gray)[0]

    # Set target brightness (adjust as needed)
    target_brightness = 128  # Aim for mid-range brightness

    # Calculate gain adjustment factor
    gain_factor = target_brightness / average_brightness

    # Apply gain to frame (ensure values stay within 0-255 range)
    adjusted_frame = cv2.convertScaleAbs(frame, alpha=gain_factor, beta=0)

    # Display the resulting frame
    cv2.imshow('OG', frame)
    cv2.imshow('AGC Target', adjusted_frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close windows
cap.release()
cv2.destroyAllWindows()
