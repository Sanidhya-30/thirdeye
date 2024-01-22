import cv2
import numpy as np

# Initialize video capture
cap = cv2.VideoCapture(0)

# Parameters for adaptive AGC
target_brightness = 128  # Adjust as needed

##change to tune, more the better
grid_size = 40  # Number of cells for grid-based region division
smooth_factor = 0.5  # Smoothing for temporal filtering

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Divide image into grid cells
    cell_width = gray.shape[1] // grid_size
    cell_height = gray.shape[0] // grid_size

    adjusted_cells = []  # List to store adjusted cells

    for i in range(grid_size):
        for j in range(grid_size):
            # Extract a cell from the image
            cell = gray[i * cell_height: (i + 1) * cell_height, j * cell_width: (j + 1) * cell_width]

            # Calculate average brightness of the cell
            average_brightness = cell.mean()

            # Calculate gain adjustment factor
            gain_factor = target_brightness / average_brightness

            # Apply gain to cell (ensure values stay within 0-255 range)
            adjusted_cell = cv2.convertScaleAbs(cell, alpha=gain_factor, beta=0)

            adjusted_cells.append(adjusted_cell)

    # Combine adjusted cells back into the frame
    adjusted_frame = np.concatenate([np.concatenate(row, axis=1) for row in np.array_split(adjusted_cells, grid_size)], axis=0)

    # Display the resulting frame
    cv2.imshow('Adaptive Region-Based AGC Demo', adjusted_frame)
    cv2.imshow('OG', gray)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
