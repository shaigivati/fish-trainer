#!/usr/bin/python
import datetime
from time import gmtime, strftime


class FishLog:
    line_number=0
    track_count=0
    feed_count={'left':0,'right':0}
    
    def __init__(self, fish_name):
        '''file name- fish_name+date+time, open new file, init counters to 0'''
        
        self.fish_name=fish_name
        print 'hello_world'
        # Open a file
        filename='log/'+strftime("%Y-%m-%d %H%M%S", gmtime())+'_'+fish_name+".txt" # time+name
        self.fo = open(filename, "w")
        
    def add_tracked_point(self,x,y):
        self.fo.write(str(self.line_number)+' ') #
        self.fo.write(str(self.track_count)+' ') #
        self.fo.write(str(datetime.datetime.now().time())+' ') #
        self.fo.write('track'+' ') #
        self.fo.write(str(x)+' ') #
        self.fo.write(str(y)+' ') #
        self.fo.write('\n') #
        self.line_number=self.line_number+1
        self.track_count=self.track_count+1
        
    def add_feed(self,side):
        self.fo.write(str(self.line_number)+' ') #
        self.fo.write(str(self.feed_count[side])+' ') #
        self.fo.write(str(datetime.datetime.now().time())+' ') #
        self.fo.write('feed'+' ') #
        self.fo.write(side+' ') #
        self.fo.write('\n') #
        self.line_number=self.line_number+1
        self.feed_count[side]=self.feed_count[side]+1
        
'''mdir'''
