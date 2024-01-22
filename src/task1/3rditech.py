import cv2

# Open the webcam (default camera, index 0)
cap = cv2.VideoCapture(0)

# Check if the webcam is opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Main loop to continuously capture frames
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Check if the frame is captured successfully
    if not ret:
        print("Error: Failed to capture frame.")
        break

    # Display the captured frame (optional)
    cv2.imshow("Webcam Feed", frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()

