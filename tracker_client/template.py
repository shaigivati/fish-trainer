#!/usr/bin/env python

'''
TBD - enter output file name as arg
TBD - create templates
'''
# USAGE
# python scene_planner.py --video fish_video_example.mp4
# python scene_planner.py  # for use with camera

import argparse
import cv2
import random

# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
fish = []

cropping = False


def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, cropping

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True

    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        refPt.append((x, y))
        cropping = False



        ordered=[(min(refPt[0][0],refPt[1][0]),min(refPt[0][1],refPt[1][1]))]
        ordered.append((max(refPt[0][0],refPt[1][0]),max(refPt[0][1],refPt[1][1])))

        crop_img = image[ordered[0][1]:ordered[1][1], ordered[0][0]:ordered[1][0]]  # Crop from x, y, w, h -> 100, 200, 300, 400
        # NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]
        cv2.imwrite("template.png", crop_img)
        cv2.waitKey(0)


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help="Path to the image")
ap.add_argument("-v", "--video", help="path to the (optional) video file")
args = vars(ap.parse_args())

# load the image, clone it, and setup the mouse callback function
# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    video_capture = cv2.VideoCapture(0)

# otherwise, grab a reference to the video file
else:
    video_capture = cv2.VideoCapture(args["video"])

ret, image = video_capture.read()

if(image is None):#check for empty frames
    print 'No Image'


# image = cv2.imread(args["image"])
clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)

# keep looping until the 'c' key is pressed
while True:

    # Write Text
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    fontColor = (255, 255, 255)
    lineType = 2

    cv2.putText(image, 'please mark your tanks',(50,50),font,fontScale,fontColor,lineType)
    cv2.putText(image, 'press "c" to finish and "r" to reset',(50,100),font,fontScale,fontColor,lineType)
    ''
    # display the image and wait for a keypress
    cv2.imshow("image", image)
    key = cv2.waitKey(1) & 0xFF

    # if the 'r' key is pressed, reset the cropping region
    if key == ord("r"):
        image = clone.copy()

    # if the 'c' key is pressed, break from the loop
    elif key == ord("c"):
        break

# if there are two reference points, then crop the region of interest
# from the image and display it

if len(refPt) == 2:

    #thefile = open('test.txt', 'w')

    for fishy in fish:
        print fishy
        thefile.write("%s\n" % fishy)

# close all open windows
cv2.destroyAllWindows()
