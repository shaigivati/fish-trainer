from __future__ import print_function
import RPi.GPIO as GPIO ## Import GPIO library
import time ## Import 'time' library. Allows us to use 'sleep'
import sys


pin_enbl = 36

pin_slp_left  = 11
pin_slp_right = 13

pin_left  = 37 #change to 15
pin_right = 38 # 

##time_to_sleep=0.8/1000.0 #(0.005) - 5ms
time_to_sleep=0.05/1000.0 #(0.005) - 5ms

GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
## Setup GPIO Pins to OUT
GPIO.setup(pin_left, GPIO.OUT) 
GPIO.setup(pin_right, GPIO.OUT)
GPIO.setup(pin_slp_left, GPIO.OUT)
GPIO.setup(pin_slp_right, GPIO.OUT)
GPIO.setup(pin_enbl, GPIO.OUT)

##Define a function named Blink()
def spin(pin_num, iter_num):
    print ("pin " + str(pin_num) + "-->" ,end='') ## Print current loop

    GPIO.output(pin_enbl,True) #pull slp pin to HIGH
    time.sleep(5*time_to_sleep)## slp shutdwon Wait

    for i in range(iter_num): #53.3 for big pill # 133 for pill device# 1600 for archimeds ### one step is 1.8 degrees
        GPIO.output(pin_num,True)## Switch on pin
        #time.sleep(0.0005)## Wait
        time.sleep(time_to_sleep)## Wait
        GPIO.output(pin_num,False)## Switch off pin
        #time.sleep(0.0005)## Wait
        time.sleep(time_to_sleep)## Wait
    time.sleep(time_to_sleep)
    GPIO.output(pin_enbl,False) #pull slp pin to HIGH
    time.sleep(50*time_to_sleep)## sleep back Wait
    destruct()
    print ("Done",end='') ## When loop is complete, print "Done"
	
def destruct():
	GPIO.cleanup()
	return

def find_slp_pin(_pin_num):
    if _pin_num==pin_left:
        pin_to_return=pin_slp_left
    if _pin_num==pin_right:
        pin_to_return=pin_slp_right
    return pin_to_return

spin(int(sys.argv[1]),int(sys.argv[2])) # uncomment for fast testing
