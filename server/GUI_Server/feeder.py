from __future__ import print_function
import RPi.GPIO as GPIO ## Import GPIO library
import time ## Import 'time' library. Allows us to use 'sleep'
from collections import defaultdict

import sys

time_to_sleep=0
#pin_enbl = 36
#pin_left  = 38 #change to 15
#pin_right = 37 #

class Feeder:
    def __init__(self, pins):
        global time_to_sleep
        time_to_sleep=0.25/1000.0 #(0.005) - 5ms
        print('feeder init --', end='')
        GPIO.setmode(GPIO.BCM) ## Use board pin numbering
        self.program_step = defaultdict(list) #for later use
        for pin in pins:
            print (' pin:{0} '.format(pin), end='')
            #print ('')
            if not int(pin) == 0:
                GPIO.setup(int(pin), GPIO.OUT)

    def add_program_step(self, step_no, step_action, step_value):
        self.program_step[step_no].append([step_action , step_value])
        print ('added, program_step now:')
        for i in self.program_step.items():
            print(i)
        print ('{0}:{1}-{2}'.format(self.program_step[1,1], self.program_step[1,2], self.program_step[1,3]))
        print ('end')
        return 'ok'

    ##Define a function named Blink()
    def spin(self, pin_num, steps, en_pin):
        print ('pin {}-->'.format(str(pin_num)),end='') ## Print current loop
        print ('steps:{}, en:{}'.format(steps, en_pin))
        GPIO.output(en_pin,True) #pull slp pin to HIGH
        time.sleep(time_to_sleep)## slp shutdwon Wait
        for i in range(steps): #53.3 for big pill # 133 for pill device# 1600 for archimeds ### one step is 1.8 degrees
            GPIO.output(pin_num,True)## Switch on pin
            time.sleep(time_to_sleep)## Wait
            GPIO.output(pin_num,False)## Switch off pin
            time.sleep(time_to_sleep)## Wait
        time.sleep(time_to_sleep)
        GPIO.output(en_pin,False) #pull slp pin to HIGH
        time.sleep(time_to_sleep)## sleep back Wait
        print ("Done",end='') ## When loop is complete, print "Done"
        return 'Done'

    def spin_program(self, pin_num, pin_direction, en_pin):
        pass

    def destruct():
        GPIO.cleanup()
        return


# spin(16,int(sys.argv[1])) # uncomment for fast testing
