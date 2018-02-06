#!/usr/bin/env python


class Tank:
	
	def __init__(self, fid, width): # pin_num - set in config file on pi
		self.fid   = fid
		self.width = width
		self.side = None
		
	
	def decide(self, x):
		if( x < self.width/4 and not self.side == 'left' ):
			self.side = 'left'
			return 'left'
		
		elif( x > self.width*3/4 and not self.side == 'right'):
			self.side = 'right'
			return 'right'
			
		return None
		