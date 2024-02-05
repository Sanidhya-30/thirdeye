import cv2
import numpy as np
import time

# ----------------------------- SOME CONSTANTS  -------------------------

mouse_click = (-1, -1)
radius = 2
font = cv2.FONT_HERSHEY_SIMPLEX
color_text = (0, 255, 0)  # green
color_circle = (0, 255, 255)  # yellow
thickness = 3
lock_status = "LOCKED"



# ----------------------------- MOUSECLICK CALLBACK  -------------------------

def onMouseClick(event, x, y, flags, param):
    global mouse_click
    if event == cv2.EVENT_LBUTTONDOWN:
        mouse_click = (x, y)
        print(mouse_click)     
        # lock_status = "LOCKED"




# ----------------------------- DRAW CIRCLE  -------------------------

def draw_circle(frame):
    global mouse_click
    cv2.circle(frame, mouse_click, radius, color_circle, thickness)




# ----------------------------- PUT TEXT IN FRAME  -------------------------

def frame_text(frame, fps):
    global lock_status
    cv2.putText(frame, lock_status, ((frame.shape[0] // 2), (3*frame.shape[1] // 4)-20), font, 1, color_text, thickness)

    # line
    p1, p2, p3, p4 = (mouse_click[0], 0), (frame.shape[1], mouse_click[1]), (mouse_click[0], frame.shape[0]), (0, mouse_click[1])
    cv2.line(frame, p1, p3, (255, 0, 0), thickness, cv2.LINE_4)
    cv2.line(frame, p2, p4, (255, 0, 0), thickness, cv2.LINE_4)




# ----------------------------- CALCULATE FPS  -------------------------

def cal_fps(frame, fps):
    global last_time  # Declare last_time as a global variable
    current_time = time.time()
    elapsed_seconds = current_time - last_time
    last_time = current_time

    # Update FPS using weighted average
    fps = (0.85 / elapsed_seconds) + ((1 - 0.85) * fps)

    # fps
    cv2.putText(frame, "FPS: " + str(int(fps)), (10, 30), font, 1, color_text, thickness)

    return fps


# ----------------------------- MAIN -------------------------

def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error opening camera!")
        exit()

    # frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fps = 0
    global last_time 
    last_time = time.time()

    (grabbed, frame) = cap.read()
    print(frame.shape)

    while (cap.isOpened()):
        (grabbed, frame) = cap.read()

        cv2.namedWindow("Display Window")
        cv2.setMouseCallback("Display Window", onMouseClick)

        fps = cal_fps(frame, fps)


        # if not (0 <= mouse_click[0] < frame.shape[1] - 20 and 0 <= mouse_click[1] < frame.shape[0] - 20):
        frame_text(frame, fps)
        draw_circle(frame)

        cv2.imshow("Display Window", frame)

        # Check for user input to exit the loop
        key = cv2.waitKey(1)
        if key == 27:  # 'Esc' key
            break

    # Release the camera and close the window after exiting the loop
    cap.release()
    cv2.destroyAllWindows()  

if __name__ == "__main__":
    main()