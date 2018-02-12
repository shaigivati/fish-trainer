#!/usr/bin/env python



# USAGE
# python track_fish.py --video fish_video_example.mp4
# python track_fish.py  # for use with camera

# sys.path.append('C:/Users/Owner/PycharmProjects/deepgaze')


import cv2
import numpy as np
from deepgaze.color_detection import BackProjectionColorDetector
from deepgaze.mask_analysis import BinaryMaskAnalyser
from deepgaze.motion_tracking import ParticleFilter
import argparse
from tracker_client.fish_tank import Tank
from tracker_client.fish_client import FishClient

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",help="path to the (optional) video file")
ap.add_argument("-f", "--file", required=True,help="path to scene file")
args = vars(ap.parse_args())

fish_client = FishClient()

with open(args["file"]) as f:
	lines = f.read().splitlines()

fish= []
for line in lines:
	fish.append(eval(line))

print fish
	
# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	video_capture = cv2.VideoCapture(0)

# otherwise, grab a reference to the video file
else:
	video_capture = cv2.VideoCapture(args["video"])
	
#fourcc = cv2.cv.CV_FOURCC(*'XVID')


template = cv2.imread('template.png')
# cv2.imshow("image", template)
# cv2.waitKey(0)
print '1'
#Filter parameters
tot_particles = 3000
#Standard deviation which represent how to spread the particles
#in the prediction phase.
std = 25 
#Probability to get a faulty measurement
noise_probability = 0.15 #in range [0, 1.0]

out=[]
width=[]
height=[]
my_mask_analyser=[]
my_back_detector=[]
my_particle=[]
tank= []

id = 0
for fishy in fish: 
	print '2'
	width.append(fishy['right'] -fishy['left']);
	height.append(fishy['lower'] -fishy['upper']);
	#out.append(cv2.VideoWriter("./fish"+str(id)	+".avi", fourcc, 25.0, (width[id],height[id])))

	print 'width: {0}, height: {1}'.format(width[id],height[id])
	#print(width,height)

	#Declaring the binary mask analyser object
	my_mask_analyser.append(BinaryMaskAnalyser())

	#Defining the deepgaze color detector object
	my_back_detector.append(BackProjectionColorDetector())
	my_back_detector[id].setTemplate(template) #Set the template 

	my_particle.append(ParticleFilter(width[id], height[id], tot_particles))
	tank.append(Tank(id, width[id]))
	id= id+1



while(True):

	# Capture frame-by-frame
	ret, frame = video_capture.read()
	if(frame is None):
		print 'No Image'
		break #check for empty frames

	id = 0
	for fishy in fish:
		frame_cut = frame[fishy['upper']:fishy['lower'], fishy['left']:fishy['right']]
		# cv2.imshow("image", frame_cut)
		# cv2.waitKey(0)
			
		#Return the binary mask from the backprojection algorithm
		frame_mask = my_back_detector[id].returnMask(frame_cut, morph_opening=True, blur=True, kernel_size=5, iterations=2)

		if(my_mask_analyser[id].returnNumberOfContours(frame_mask) > 0):
			#Use the binary mask to find the contour with largest area
			#and the center of this contour which is the point we
			#want to track with the particle filter
			x_rect,y_rect,w_rect,h_rect = my_mask_analyser[id].returnMaxAreaRectangle(frame_mask)
			x_center, y_center = my_mask_analyser[id].returnMaxAreaCenter(frame_mask)

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
		my_particle[id].predict(x_velocity=0, y_velocity=0, std=std)

		#Drawing the particles.
		my_particle[id].drawParticles(frame_cut)

		#Estimate the next position using the internal model
		x_estimated, y_estimated, _, _ = my_particle[id].estimate()
		cv2.circle(frame_cut, (x_estimated, y_estimated), 3, [0,255,0], 5) #GREEN dot
		cv2.imshow("image", frame_cut)
		cv2.waitKey(1)
		#Update the filter with the last measurements
		my_particle[id].update(x_center, y_center)
		
		#Resample the particles
		my_particle[id].resample()
		
		#print '{0},{1},{2}'.format(id, x_estimated, y_estimated)
		feed_side = tank[id].decide(x_estimated)
		if (feed_side != None):
			fish_client.send(id, feed_side)
					
		#Writing in the output file
		#out[id].write(frame_cut)
		
		id= id+1
  #  if cv2.waitKey(1) & 0xFF == ord('q'): break #Exit when Q is pressed

#Release the camera
#video_capture.release()
print("Bye...")


