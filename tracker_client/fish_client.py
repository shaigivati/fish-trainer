#!/usr/bin/env python

import socket
import json

class FishClient:
	
	def __init__(self):
		#self.TCP_IP = '132.72.44.66'
		self.TCP_IP = '132.72.91.148'
		#self.TCP_IP = '132.73.194.80'
		self.TCP_PORT = 50007
		self.BUFFER_SIZE = 1024
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((self.TCP_IP, self.TCP_PORT))
	def send(self,id, side):
		
		data=json.dumps({'id':id,'side':side})
		self.s.send(data)
		data = self.s.recv(self.BUFFER_SIZE)

		print "received data:", data
		
	def kill(self):
		self.s.close()