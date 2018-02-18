#!/usr/bin/env python

from __future__ import print_function	#to 'print' without newline
import sys
import socket
import argparse
import json
import feeder
import thread 							#for multithread func. (keyboard input)

def read_key():
	import termios
	import sys
	fd = sys.stdin.fileno()
	old = termios.tcgetattr(fd)
	new = termios.tcgetattr(fd)
	new[3] &= ~(termios.ICANON | termios.ECHO) # c_lflags
	c = None
	try:
		termios.tcsetattr(fd, termios.TCSANOW, new)
		c = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSANOW, old)
	return c

def input_thread():

	#global key_pressed
	while True:
		key_pressed=read_key()
		print ("Key pressed- %s" % key_pressed)
		#print(key_pressed)
		if (key_pressed=="q" or key_pressed=="Q"):
			thread.interrupt_main()
			break

def main_server():
	# construct the argument parser and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-f", "--file", required=True,help="path to scene file")
	args = vars(ap.parse_args())



	with open(args["file"]) as f:
		lines = f.read().splitlines()

	fish= []
	for line in lines:
		fish.append(eval(line))

	#TCP_IP = '132.72.44.66'
	TCP_IP = ''
	TCP_PORT = 5008
	BUFFER_SIZE = 1024  #was 20-  Normally 1024, but we want fast response

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((TCP_IP, TCP_PORT))
	s.listen(1)
	print ("Server is up and waiting for connections")

	#while 1:

	s.settimeout(1)
	try:
		conn, addr = s.accept()
		print ("Connection address:", addr)
		s.settimeout(None)
		# while 1:
		try:
			data = conn.recv(BUFFER_SIZE)
			# if not data: break
			if data:
				# id=data.id
				json_acceptable_string = data.replace("'", "\"")
				d = json.loads(json_acceptable_string)

				id = d["id"]
				side = d['side']
				print (side)
				print (fish[id][side])
				feeder.spin(fish[id][side], 53)
				# print "server received data:", data
				conn.send(side)  # echo
		except:
			# check if error raised because computer disconnected
			str_err = str(sys.exc_info())
			err_socket = []
			err_socket.append(str_err.find("socket.error") is not -1)
			err_socket.append(str_err.find("Connection reset by peer") is not -1)
			if (err_socket[0] and err_socket[1]):
				print ("socket.err - client disconnected")
				print ("Server is up and waiting for connections")
				pass
	except:
		str_err = str(sys.exc_info())
		err_socket = []
		err_socket.append(str_err.find("socket.timeout") is not -1)
		if (err_socket[0]):
			print (".", end='')
			pass



		#print "Unexpected error: [0]-", sys.exc_info()[0], " [1]-", sys.exc_info()[1], " [2]-", sys.exc_info()[2]
	#conn.close()

def main():
	try:
		thread.start_new_thread(input_thread, ())       # ADDED
		i=0
		while True: #loop
			main_server()
			i+=1
			if (i>200):
				print ("main loop")
				i=0

	except KeyboardInterrupt:                           # ADDED
		print ("Quit")
		conn.close()
		sys.exit(0)


if  __name__ =='__main__':
	main()

#TBD-
# make sever into loop
# heck other IP
# why server needs ip?

# create both of this as classes and than -
# track fish import client
# feeder import server or server import feeder 