'''
Inspired by pyimagesearch : Ball tracking with OpenCV
Link: https://pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/
'''

# USAGE: Put the following commands for saving the file in the same location as input file
# python bg_subtract.py --video file_name.mp4 (if input video is taken from file)
# python bg_subtract.py (if using a webcam)

# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import time

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
                help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=5,
                help="max buffer size")
ap.add_argument("-f", "--fps", type=int, default=20,
                help="FPS of output video")
ap.add_argument("-c", "--codec", type=str, default="mp4v",
                help="codec of output video")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "red"
# and "green" and "white" ball in the HSV color space,
# then initialize the list of tracked points
# color_range = {'red': {'lower': (0, 185, 135), 'upper': (255, 255, 255)},
#                'green': {'lower': (20, 70, 100), 'upper': (80, 255, 255)},
#                'white': {'lower': (16, 0, 100), 'upper': (60, 50, 255)}}

# color_range = {'orange': {'lower': (0, 100, 200), 'upper': (255, 255, 255)},
#                'yellow': {'lower': (20, 65, 140), 'upper': (50, 255, 255)},
#                'green': {'lower': (40, 25, 70), 'upper': (80, 255, 255)}}

# HSV colour values for cascade.mp4 video
color_range = {'orange': {'lower': (0, 130, 170), 'upper': (255, 255, 255)},
               'yellow': {'lower': (20, 65, 140), 'upper': (50, 255, 255)},
               'green': {'lower': (40, 25, 70), 'upper': (80, 255, 255)}}

tracking_points = {}

for color in color_range:
    tracking_points[color] = deque(maxlen=args["buffer"])
    counter = 0
    (dX, dY) = (0, 0)
    direction = ""

# if a video path was not supplied, grab the reference to the webcam
if not args.get("video", False):
    vs = cv2.VideoCapture(0)
# otherwise, grab a reference to the video file
else:
    vs = cv2.VideoCapture(args["video"])

# We need to check if camera is opened previously or not
if not vs.isOpened():
    print("Error reading video file")

# allow the camera or video file to warm up
time.sleep(2.0)

# initialize the FourCC, video writer, dimensions of the frame
# like width, height and aspect ratio
fourcc = cv2.VideoWriter_fourcc(*args["codec"])
frame_width = int(vs.get(3))
frame_height = int(vs.get(4))
size = (frame_width, frame_height)
aspect_ratio = float(frame_height/frame_width)
writer = cv2.VideoWriter('cascade_saved2.mp4', fourcc, 35, (600, int(600 * aspect_ratio)), True)


# keep looping
while True:
    # grab the current frame
    ret, frame = vs.read()
    # # handle the frame from VideoCapture or VideoStream
    # frame = frame[1] if args.get("video", False) else frame
    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if frame is None:
        break
    # # resize the frame, blur it, and convert it to the HSV
    # # color space
    frame = imutils.resize(frame, width=600)
    # print("frame shape: ", frame.shape)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.waitKey(5)

    for color in color_range:
        mask = cv2.inRange(hsv, color_range[color]['lower'],
                           color_range[color]['upper'])
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            if radius > 10:
                cv2.circle(frame, (int(x), int(y)), int(radius),
                           (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
                tracking_points[color].appendleft(center)
            else:
                tracking_points[color] = deque(maxlen=args["buffer"])
        for i in range(1, len(tracking_points[color])):
            if tracking_points[color][i - 1] is None or tracking_points[color][i] is None:
                continue
            # check to see if enough points have been accumulated in
            # the buffer
            if counter >= 10 and i == 10 and tracking_points[color][i-10] is not None:
                # compute the difference between the x and y
                # coordinates and re-initialize the direction
                # text variables
                dX = tracking_points[color][i-10][0] - tracking_points[color][i][0]
                dY = tracking_points[color][i-10][1] - tracking_points[color][i][1]
                (dirX, dirY) = ("", "")
                # ensure there is significant movement in the
                # x-direction
                if np.abs(dX) > 20:
                    dirX = "East" if np.sign(dX) == 1 else "West"
                # ensure there is significant movement in the
                # y-direction
                if np.abs(dY) > 20:
                    dirY = "North" if np.sign(dY) == 1 else "South"
                # handle when both directions are non-empty
                if dirX != "" and dirY != "":
                    direction = "{}-{}".format(dirY, dirX)
                # otherwise, only one direction is non-empty
                else:
                    direction = dirX if dirX != "" else dirY

            thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
            cv2.line(frame, tracking_points[color][i - 1],
                     tracking_points[color][i], (0, 0, 255), thickness)
        # show the movement deltas and the direction of movement on
        # the frame
        cv2.putText(frame, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    0.65, (0, 0, 255), 3)
        cv2.putText(frame, "dx: {}, dy: {}".format(dX, dY),
                    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.35, (0, 0, 255), 1)
    if ret:
        # Write the frame into the file 'filename.avi'
        writer.write(frame)
        # Display the frame saved in the file
        cv2.imshow('Frame', frame)
        key = cv2.waitKey(1) & 0xFF
        counter += 1
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
    else:
        break

# When everything done, release the video capture and video write objects
cv2.destroyAllWindows()
vs.release()
writer.release()

print("The video was successfully saved")
