import cv2
import time

# Function to calculate FPS using the basic method
def calculate_basic_fps(video_capture):
    start_time = time.time()
    frame_count = 0

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        frame_count += 1
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    end_time = time.time()
    elapsed_time = end_time - start_time
    basic_fps = frame_count / elapsed_time
    print(f"Basic FPS: {basic_fps}")

# Function to calculate FPS using fixed time interval method
def calculate_fixed_interval_fps(video_capture):
    start_time = time.time()
    frame_count = 0
    interval_duration = 5  # seconds
    interval_start_time = start_time

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        frame_count += 1
        cv2.imshow('Video', frame)

        current_time = time.time()
        if current_time - interval_start_time > interval_duration:
            elapsed_time = current_time - start_time
            fixed_interval_fps = frame_count / elapsed_time
            print(f"Fixed Interval FPS: {fixed_interval_fps}")

            # Reset counters for the next interval
            frame_count = 0
            start_time = time.time()
            interval_start_time = start_time

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Function to calculate FPS using adaptive moving average method
def calculate_adaptive_average_fps(video_capture):
    alpha = 0.2  # Exponential smoothing factor
    start_time = time.time()
    frame_count = 0
    accumulated_frame_time = 0

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        frame_count += 1
        cv2.imshow('Video', frame)

        current_time = time.time()
        time_difference = current_time - start_time
        accumulated_frame_time += time_difference
        instantaneous_fps = frame_count / time_difference
        adaptive_average_fps = frame_count / accumulated_frame_time

        print(f"Adaptive Average FPS: {adaptive_average_fps}")

        start_time = current_time
        frame_count = 0

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Function to calculate FPS using running average method
def calculate_running_average_fps(video_capture):
    alpha = 0.2  # Exponential smoothing factor
    running_average_fps = 0
    start_time = time.time()
    frame_count = 0

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        frame_count += 1
        cv2.imshow('Video', frame)

        current_time = time.time()
        time_difference = current_time - start_time
        instantaneous_fps = frame_count / time_difference
        running_average_fps = (1 - alpha) * running_average_fps + alpha * instantaneous_fps

        print(f"Running Average FPS: {running_average_fps}")

        start_time = current_time
        frame_count = 0

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Open a video capture object (you can replace 'video.mp4' with your video file or camera index)
video_capture = cv2.VideoCapture('video.mp4')

# Uncomment the function you want to use for FPS calculation
# calculate_basic_fps(video_capture)
# calculate_fixed_interval_fps(video_capture)
# calculate_adaptive_average_fps(video_capture)
# calculate_running_average_fps(video_capture)

# Release the video capture object and close the OpenCV windows
video_capture.release()
cv2.destroyAllWindows()
