#!/usr/bin/env python

import cv2

stop_training=False
video_capture = None

#tank_config='../tracker/tank_config.txt'
def init_tracking(tank_config='tracker/tank_config.txt',video=None):
    global video_capture, fish, width, height, tank, fgbg
    fish = []
    width = []
    height = []
    tank = []
    fgbg = []

    with open(tank_config) as f:
        lines = f.read().splitlines()
    for line in lines:
        fish.append(eval(line))
    print fish

    # if a video path was not supplied, grab the reference to the webcam
    if video is None:
        video_capture = cv2.VideoCapture(0)
    # otherwise, grab a reference to the video file
    else:
        video_capture = cv2.VideoCapture(video)

    id = 0
    for fishy in fish:
        fgbg.append(cv2.bgsegm.createBackgroundSubtractorMOG())
        width.append(fishy['right'] - fishy['left'])
        height.append(fishy['lower'] - fishy['upper'])
        tmp_str = 'width: {0}, height: {1}'.format(width[id], height[id])
        print tmp_str

        id = id + 1

    return width

def __del__():  #Destroy
    print ('track_fish closed')
    cv2.destroyAllWindows()

def track_loop(cb): #cb is an object that has a do() function in the calling script
    global stop_training
    #while True:
    while stop_training==False:
        cb.time()
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        if frame is None:
            print 'No Image'
            break  # check for empty frames

        id = 0
        for fishy in fish:
            frame_cut = frame[fishy['upper']:fishy['lower'], fishy['left']:fishy['right']]
            fgmask = fgbg[id].apply(frame_cut)
            fgmask = cv2.erode(fgmask, None, iterations=2)
            mask = cv2.dilate(fgmask, None, iterations=2)
            cv2.imshow("image" + str(id), frame_cut)
            cv2.imshow("mask"+str(id), fgmask)
            cv2.waitKey(1)

            # find contours in the mask and initialize the current
            # (x, y) center of the ball
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

            max_rad=0
            for cntr in cnts:
                ((x, y), radius) = cv2.minEnclosingCircle(cntr)
                if radius > max_rad:
                    largest_cntr = cntr
                    max_rad = radius
            # check if largest_cntr is set
            if len(cnts) > 0:
                ((x, y), radius) = cv2.minEnclosingCircle(largest_cntr)
                cv2.circle(frame_cut, (int(x), int(y)), int(radius), (0, 255, 255), 2)  # show radius for debbuging
                cv2.imshow("image"+str(id), frame_cut)
                cv2.waitKey(1)

                if cb is not None:
                    cb.do(x, y, id)


            id = id + 1
        # TBD - inclear where to put
        # if cv2.waitKey(1) & 0xFF == ord('q'): break #Exit when Q is pressed
    #print ('track_fish closed')
    __del__()
    return 0

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", help="path to the (optional) video file")
    ap.add_argument("-f", "--file", help="path to scene file")
    args = vars(ap.parse_args())
    init_tracking(args["file"])
    track_loop(None)

    # Release the camera
    video_capture.release()
    print("Bye...")






