# DFKI-multi_ball_tracking
This project was done to detect tracking and position of multiple balls juggled by a robot. The repository includes the implementation of ball tracking with OpenCV from pyimagesearch and has been modified according to the required use-case scenario. The different scenarios are defined by the use of number of balls for the detection of outer boundary and the center of the balls to detect tracking in 3D space.
The repository is inspired, modified and implemented from 'pyimagesearch : Ball tracking with OpenCV https://pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/'
The scenarios are termed as box, cascade, millsmess and trickmix. The level of difficulty increases with each scenario by its movement and the number of balls to be detected in physical space.

# Installation and Requirements
The repository requires OpenCV, imutils, deque, matplotlib, pandas, numpy and other libraries for running the code and is possible to run to with both --Python 2.7 and --Python3. If you need to just detect and track the colors of multiple balls, it can be done by running the 'multi_color_tracking.py' file. The 'ball_tracking.py' and 'two_color_tracking.py' scripts are used to run the use-case scenarios of one and two ball detections.

# Centroid and Range Detector
The scripts 'plot_centroids.py' and 'range_detector.py' are used to convert color spaces of RGB and HSV to each other for the purpose of image processing. The file path needs to be specified in the script.

# Writing result videos
The resulting videos with detected centroids and tracking lines of single, two or multiple balls in space can be written with 'write_video.py'
