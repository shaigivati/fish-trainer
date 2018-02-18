#!/usr/bin/env python

import sys
import socket
import argparse
import json
import feeder


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
print 'Server is up and waiting for connections'

while 1:
	conn, addr = s.accept()
	print 'Connection address:', addr
	while 1:
		try:
			data = conn.recv(BUFFER_SIZE)
			if not data: break
			#id=data.id
			json_acceptable_string = data.replace("'", "\"")
			d = json.loads(json_acceptable_string)
		
			id = d["id"]
			side=d['side']
			print side
			print fish[id][side]
			feeder.spin(fish[id][side],53)
			#print "server received data:", data
			conn.send(side)  # echo
		except:
			str_err=str(sys.exc_info())
			print "error: ", str_err
			print str_err[0].find("socket.error"), " , ", str_err[2].find("Connection reset by peer")
			#if (str_err[0].find("socket.error") is not -1): print "s.err"
			#if (str_err[2].find("Connection reset by peer") is not -1): print "peer reset"
			#print "Unexpected error: [0]-", sys.exc_info()[0], " [1]-", sys.exc_info()[1], " [2]-", sys.exc_info()[2]
	conn.close()


#TBD-
# make sever into loop
# heck other IP
# why server needs ip?

# create both of this as classes and than -
# track fish import client
# feeder import server or server import feeder 