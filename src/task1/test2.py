import cv2
import time
import matplotlib.pyplot as plt

# Function to calculate FPS using the basic method
def calculate_basic_fps(video_capture):
    start_time = 0
    frame_count = 0
    bfps=[]

    while True:
        ret, frame = video_capture.read()
        
        if not ret:
            break
        
        if frame == True:
            print(frame)
            frame_count += 1
            end_time = time.time()
            elapsed_time = end_time - start_time
            basic_fps = frame_count / elapsed_time
            bfps.append(basic_fps)
        print(f"Basic FPS: {basic_fps}")
    
    return bfps

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
        #cv2.imshow('Video', frame)

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
        #cv2.imshow('Video', frame)

        current_time = time.time()
        time_difference = current_time - start_time
        instantaneous_fps = frame_count / time_difference
        running_average_fps = (1 - alpha) * running_average_fps + alpha * instantaneous_fps

        print(f"Running Average FPS: {running_average_fps}")

        start_time = current_time
        frame_count = 0

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

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
        #cv2.imshow('Video', frame)

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

# Open a video capture object (you can replace 'video.mp4' with your video file or camera index)
video_capture = cv2.VideoCapture(0)
# video_capture = cv2.VideoCapture('video0.mp4')
if not video_capture.isOpened():
    print("Error: Couldn't open the video file.")
    exit()
print(video_capture)

calculate_basic_fps(video_capture)
# calculate_fixed_interval_fps(video_capture)
# calculate_adaptive_average_fps(video_capture)
# calculate_running_average_fps(video_capture)
## Uncomment the function you want to use for FPS calculation
bfps    = calculate_basic_fps(video_capture)
# fifps[]   = calculate_fixed_interval_fps(video_capture)
# raps[]    = calculate_running_average_fps(video_capture)
# amaps[]   = calculate_adaptive_average_fps(video_capture)

# # Create a Matplotlib figure and is for real-time plotting
# plt.plot(bfps)
# plt.title('FPS Over Time')
# plt.xlabel('Time (s)')
# plt.ylabel('FPS')
# plt.show()


# Release the video capture object and close the OpenCV windows
video_capture.release()
cv2.destroyAllWindows()