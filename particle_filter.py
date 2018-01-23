#!/usr/bin/env python

import cv2
import numpy as np
from deepgaze.color_detection import BackProjectionColorDetector
from deepgaze.mask_analysis import BinaryMaskAnalyser
from deepgaze.motion_tracking import ParticleFilter

USE_WEBCAM = False

class Filter:
    
    
    def __init__(self, template, roi):
        self.template = template
        self.roi = roi
        print self.roi
        
        if(USE_WEBCAM == False):
            video_capture = cv2.VideoCapture("/root/mnt_ws/fish/2fish_short.mp4")
        else:
            video_capture = cv2.VideoCapture(0) #Open the webcam
        # Define the codec and create VideoWriter object
        fourcc = cv2.cv.CV_FOURCC(*'XVID')
        out = cv2.VideoWriter("./cows_output3.avi", fourcc, 25.0, (1920,1080))

        #Declaring the binary mask analyser object
        my_mask_analyser = BinaryMaskAnalyser()

        #Defining the deepgaze color detector object
        my_back_detector = BackProjectionColorDetector()
        my_back_detector.setTemplate(self.template) #Set the template 

        #Filter parameters
        tot_particles = 3000
        #Standard deviation which represent how to spread the particles
        #in the prediction phase.
        std = 25 
        my_particle = ParticleFilter(1920, 1080, tot_particles)
        #Probability to get a faulty measurement
        noise_probability = 0.15 #in range [0, 1.0]

        while(True):

            # Capture frame-by-frame 
            ret, frame = video_capture.read()
            if(frame is None): break #check for empty frames
            frame = frame[0:1080, 0:1920] 

            #Return the binary mask from the backprojection algorithm
            frame_mask = my_back_detector.returnMask(frame, morph_opening=True, blur=True, kernel_size=5, iterations=2)
            if(my_mask_analyser.returnNumberOfContours(frame_mask) > 0):
                #Use the binary mask to find the contour with largest area
                #and the center of this contour which is the point we
                #want to track with the particle filter
                x_rect,y_rect,w_rect,h_rect = my_mask_analyser.returnMaxAreaRectangle(frame_mask)
                x_center, y_center = my_mask_analyser.returnMaxAreaCenter(frame_mask)
                #Adding noise to the coords
                coin = np.random.uniform()
                if(coin >= 1.0-noise_probability): 
                    x_noise = int(np.random.uniform(-300, 300))
                    y_noise = int(np.random.uniform(-300, 300))
                else: 
                    x_noise = 0
                    y_noise = 0
                x_rect += x_noise
                y_rect += y_noise
                x_center += x_noise
                y_center += y_noise
        #        cv2.rectangle(frame, (x_rect,y_rect), (x_rect+w_rect,y_rect+h_rect), [255,0,0], 2) #BLUE rect

            #Predict the position of the target
            my_particle.predict(x_velocity=0, y_velocity=0, std=std)

            #Drawing the particles.
            my_particle.drawParticles(frame)

            #Estimate the next position using the internal model
            x_estimated, y_estimated, _, _ = my_particle.estimate()
            cv2.circle(frame, (x_estimated, y_estimated), 3, [0,255,0], 5) #GREEN dot

            #Update the filter with the last measurements
            my_particle.update(x_center, y_center)

            #Resample the particles
            my_particle.resample()
            #Writing in the output file
            out.write(frame)

          #  if cv2.waitKey(1) & 0xFF == ord('q'): break #Exit when Q is pressed


        #Release the camera
        video_capture.release()
        print("Bye...")

 
fish_one = Filter(cv2.imread('/root/mnt_ws/fish/template.png'),[1,2,3,4]) 