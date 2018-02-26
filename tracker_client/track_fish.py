#!/usr/bin/env python

# USAGE
# python track_fish.py --video fish_video_example.mp4
# python track_fish.py --file path_to_tank_config --log name_of_fish
import sys
import cv2
import numpy as np
from deepgaze.color_detection import BackProjectionColorDetector
from deepgaze.mask_analysis import BinaryMaskAnalyser
from deepgaze.motion_tracking import ParticleFilter
import argparse
from tracker_client.fish_tank import Tank
from tracker_client.fish_client import FishClient
from tools import fishlog
import threading
import os
import multiprocessing


import time


class Counter(object):
    def __init__(self, start = 0):
        self.lock = threading.Lock()
        self.value = start

    def increment(self):
        logging.debug('Waiting for a lock')
        self.lock.acquire()
        try:
            logging.debug('Acquired a lock')
            self.value = self.value + 1
        finally:
            logging.debug('Released a lock')
            self.lock.release()


def main_tf(lst_args, in_queue):
	global counter
	# construct the argument parser and parse the arguments
	#for arg in sys.argv[1:]:
	#	print arg
	#ap = argparse.ArgumentParser()

	#ap.add_argument("-v", "--video",help="path to the (optional) video file")
	#ap.add_argument("-f", "--file", required=True,help="path to scene file")
	#ap.add_argument("-log", "--log", required=True,help="path to scene file")
	#args = vars(ap.parse_args())
	#print "main:",lst_args
	time_to_sleep=1 #sec
	i_msg = 99  # TAL
	full_script_path='{}{}'.format(os.path.dirname(os.path.realpath(__file__)), '/')
	full_file_path='{}{}'.format(full_script_path, lst_args["file"])

	print('full_script_path:{}'.format(full_script_path))

	with open(full_file_path) as f:
		lines = f.read().splitlines()

	fish= []
	for line in lines:
		fish.append(eval(line))

	print fish

	# if a video path was not supplied, grab the reference to the webcam
	if not lst_args.get("video", False):
		video_capture = cv2.VideoCapture(0)

	# otherwise, grab a reference to the video file
	else:
		video_capture = cv2.VideoCapture(lst_args["video"])




	#Filter parameters
	tot_particles = 3000
	#Standard deviation which represent how to spread the particles
	#in the prediction phase.
	std = 25
	#Probability to get a faulty measurement
	noise_probability = 0.15 #in range [0, 1.0]

	template = cv2.imread('{}{}'.format(full_script_path, 'template.png'))

	full_root_script_path =  full_script_path[:full_script_path.find('tracker_client')]
	log_folder = '{}data/log/'.format(full_root_script_path)
	print('log:{}'.format(log_folder))

	logger = fishlog.FishLog(log_folder, lst_args["log"])



	out=[]
	width=[]
	height=[]
	my_mask_analyser=[]
	my_back_detector=[]
	my_particle=[]
	tank= []

	id = 0
	for fishy in fish:
		width.append(fishy['right'] -fishy['left']);
		height.append(fishy['lower'] -fishy['upper']);

		print 'width: {0}, height: {1}'.format(width[id],height[id])

		#Declaring the binary mask analyser object
		my_mask_analyser.append(BinaryMaskAnalyser())

		#Defining the deepgaze color detector object
		my_back_detector.append(BackProjectionColorDetector())
		my_back_detector[id].setTemplate(template) #Set the template

		my_particle.append(ParticleFilter(width[id], height[id], tot_particles))
		tank.append(Tank(id, width[id]))
		id= id+1


	while(True):
		#if n == None:
			#break
		#time.sleep(0.01)
		try:
			if not in_queue.empty():
				n = in_queue.get()
				print n
				if int(n)==5: break
			# Capture frame-by-frame


			ret, frame = video_capture.read()
			if(frame is None):
				print 'No Image'
				#break #check for empty frames

			id = 0
			for fishy in fish:
				frame_cut = frame[fishy['upper']:fishy['lower'], fishy['left']:fishy['right']]

				#Return the binary mask from the backprojection algorithm
				frame_mask = my_back_detector[id].returnMask(frame_cut, morph_opening=True, blur=True, kernel_size=5, iterations=2)

				if(my_mask_analyser[id].returnNumberOfContours(frame_mask) > 0):
					#Use the binary mask to find the contour with largest area
					#and the center of this contour which is the point we
					#want to track with the particle filter
					x_rect,y_rect,w_rect,h_rect = my_mask_analyser[id].returnMaxAreaRectangle(frame_mask)
					x_center = None  #TAL
					y_center = None  # TAL
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
				#while (x_center is None or y_center is None): #TAL
				#	time.sleep(time_to_sleep)
				#	print("Waiting for fish")

				my_particle[id].update(x_center, y_center)


				logger.add_tracked_point(x_center, y_center)

				#Resample the particles
				my_particle[id].resample()

				feed_side = tank[id].decide(x_estimated)
				if (feed_side != None):
					print "id:",id," side:",feed_side
					fish_client = FishClient()
					fish_client.send(id+1, feed_side)
					logger.add_feed(feed_side)


				id= id+1
		except NameError:	#TAL
			if (i_msg>100):
				print "There is fish ?..", "Cnr:" ,counter.value
				i_msg=0
			i_msg+=1
			#time.sleep(time_to_sleep)
		#else:
			#print ""
			#print "sure, it was defined."
	  #  if cv2.waitKey(1) & 0xFF == ord('q'): break #Exit when Q is pressed

		#Release the camera
		#video_capture.release()
	#print("Bye...")




counter = Counter()

if __name__ == '__main__':
	arguments = sys.argv
	file_name = arguments[0]
	arg_temp = str(arguments[1])
	arg1 = arg_temp[arg_temp.find('=')+1:]
	arg_temp = str(arguments[2])
	arg2 = arg_temp[arg_temp.find('=')+1:]
	#print ('1:{} 2:{} 3:{}'.format(file_name, arg1, arg2))

	args={"file_name" : file_name, "file" : arg1, "log" : arg2}
	#ap = argparse.ArgumentParser()
	#ap.add_argument("-v", "--video", help="path to the (optional) video file")
	#ap.add_argument("-f", "--file", required=True, help="path to scene file")
	#ap.add_argument("-log", "--log", required=True, help="path to scene file")
	#args = vars(ap.parse_args())
	#print "if:",args
	print(args)
	in_queue = multiprocessing.Queue()
	in_queue.put(1)

	main_tf(args,in_queue)
