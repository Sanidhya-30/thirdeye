import numpy as np 
import cv2 
import time 

cap = cv2.VideoCapture(1) 
prev_frame_time = 0                     # used to record the time when we processed last frame 
new_frame_time = 0                      # used to record the time at which we processed current frame 

# Reading the video file until finished 
while(cap.isOpened()): 
	
	ret, frame = cap.read() 	        # Capture frame-by-frame 
	if not ret: 	                    # if video finished or no Video Input 
		break
	font = cv2.FONT_HERSHEY_SIMPLEX     # font which we will be using to display FPS
	new_frame_time = time.time()        # time when we finish processing for this frame 

	
    # Calculating the fps 
	fps = 1/(new_frame_time-prev_frame_time) 
	prev_frame_time = new_frame_time 

	# converting the fps into integer 
	fps = int(fps) 

	# displaying the frame with fps 
	fps = str(fps) 
	cv2.putText(frame, fps, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA) 
	cv2.imshow('frame', frame)
	print(fps) 

	# press 'Q' if you want to exit 
	if cv2.waitKey(1) & 0xFF == ord('q'): 
		break
	
cap.release() 
cv2.destroyAllWindows() 
