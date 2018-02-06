#!/usr/bin/env python

import socket
import json

class FishClient:
	
	def __init__(self):
		#self.TCP_IP = '132.72.44.66'
		self.TCP_IP = '132.72.88.57'
		self.TCP_PORT = 5007
		self.BUFFER_SIZE = 1024
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((self.TCP_IP, self.TCP_PORT))
	def send(self,id, side):
		
		data=json.dumps({'id':id,'side':side})
		self.s.send(data)
		data = self.s.recv(self.BUFFER_SIZE)

		print "received data:", data
		
	def kill(self):
		s.close()