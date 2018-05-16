from __future__ import print_function
import RPi.GPIO as GPIO ## Import GPIO library
import time ## Import 'time' library. Allows us to use 'sleep'
from collections import defaultdict
import math

time_to_sleep=0
[equ_a, equ_b, equ_c] = (1/25, -2/25, 1)    #y(x) = a*(x-x0)^2 + b(x-x0) + c
#pin_enbl = 36
#pin_left  = 38 #change to 15
#pin_right = 37 #

class Feeder:
    def __init__(self, pins):
        global time_to_sleep
        self.one_deg = 1600.0/360.0
        time_to_sleep=0.25/1000.0 #(0.005) - 5ms
        print('feeder init --', end='')
        GPIO.setmode(GPIO.BCM) ## Use board pin numbering
        self.program_step = defaultdict(list) #for later use
        for pin in pins:
            print (' pin:{0} '.format(pin), end='')
            #print ('')
            if not int(pin) == 0:
                GPIO.setup(int(pin), GPIO.OUT)

    def add_program_step(self, step_no, step_action, step_value, step_velocity=10, step_accl=20):
        self.program_step[step_no].append(step_action)
        self.program_step[step_no].append(step_value)
        self.program_step[step_no].append(step_velocity)
        self.program_step[step_no].append(step_accl)

        print ("items:")
        for item in self.program_step.items():
            print ('{0}:{1}-{2} ({3},{4})'.format(item[0], item[1][0], item[1][1], item[1][2], item[1][3]))

        print ('end')
        return 'ok'

    ##Define a function named Blink()
    def spin(self, pin_num, steps, en_pin):
        print ('pin {0}-->'.format(str(pin_num)),end='') ## Print current loop
        print ('steps:{0}, en:{1}'.format(steps, en_pin))
        GPIO.output(en_pin, True) #pull slp pin to HIGH
        time.sleep(time_to_sleep)## slp shutdwon Wait
        for i in range(steps): #53.3 for big pill # 133 for pill device# 1600 for archimeds ### one step is 1.8 degrees
            GPIO.output(pin_num, True)## Switch on pin
            time.sleep(time_to_sleep)## Wait
            GPIO.output(pin_num, False)## Switch off pin
            time.sleep(time_to_sleep)## Wait
        time.sleep(time_to_sleep)
        GPIO.output(en_pin, False) #pull slp pin to HIGH
        time.sleep(time_to_sleep)## sleep back Wait
        print ("Done",end='') ## When loop is complete, print "Done"
        return 'Done'

    def spin_program(self, pin_num, pin_direction, en_pin, steps=0):

        #print('pin:{0}, direction:{1}, en:{2}'.format(str(pin_num), str(pin_direction), str(en_pin)))  ## Print current loop
        steps_to_do = int(360.0 * self.one_deg)
        if not steps == 0:
            steps_to_do = steps
            self.raw_spin(pin_num, pin_direction, en_pin, steps_to_do, 'R', 10, 0.25)
        else:
            #self.raw_spin(pin_num, pin_direction, en_pin, steps_to_do, 'R', 0.25)
            for item in self.program_step.items():
                print('{0}:{1}-{2} ({3},{4})'.format(item[0], item[1][0], item[1][1], item[1][2], item[1][3]))
                if item[1][0] == 'wait':
                    time.sleep(item[1][1])
                else:
                    direction = ((item[1][0])[0:1]).upper() #'L' or 'R'
                    steps_to_do = int(item[1][1] * self.one_deg)
                    self.raw_spin(pin_num, pin_direction, en_pin, steps_to_do, direction, item[1][2], item[1][3])

        return 'Done'

    def raw_spin(self, pin_num, pin_dir, en_pin, steps, direction, velocity, accl):
        print ("accl:{0}".format(accl))
        GPIO.output(en_pin, True) #pull slp pin to HIGH
        GPIO.output(pin_dir, direction == 'L')    #HIGH for 'L', LOW for else
        print ('steps:{0}, {1}%:{2}'.format(steps, accl, int((accl/100)*steps)))
        for i in range(steps): #53.3 for big pill # 133 for pill device# 1600 for archimeds ### one step is 1.8 degrees
            print ('{0},{1:.2f}\t\t'.format(i, self.velocity_calc(velocity, steps, accl, i)), end='')
            #if i/10 == 0: print (".", end='')
            #GPIO.output(pin_num, True)## Switch on pin
            #time.sleep(acceleration/2)## Wait
            #GPIO.output(pin_num, False)## Switch off pin
            #time.sleep(acceleration/2)## Wait
        print ("")
        GPIO.output(en_pin, False) #pull slp pin to HIGH
        GPIO.output(pin_dir, False)
        print("Done")
        return 'Done'

    def velocity_calc(self, max_velocity, total_steps, percentage, c_step):
        if c_step == 1 or c_step == 99:
            print(total_steps*(percentage/100.0))
        if (c_step <= total_steps*(percentage/100)):
            accl_pr = self.accl('up', c_step, percentage, total_steps)
            velocity = (accl_pr/100)*max_velocity
        elif (c_step >= total_steps - (total_steps*(percentage/100))):
            accl_pr = self.accl('down', c_step, percentage, total_steps)
            velocity = (accl_pr/100)*max_velocity
        else:
            velocity = max_velocity
        return velocity

    def accl(self, direction, i, percentage, total_steps):
        func=0
        try:
            if direction == 'up':
                func = math.exp((10 * i) / (2 * percentage))
            if direction == 'down':
                func = math.exp((10 * (total_steps - i) ) / (2 * percentage))
            accl = func
        except ZeroDivisionError as error:
            print ("Error: ZeroDivisionError")
            accl = func
        return accl

    def destruct():
        GPIO.cleanup()
        return


# spin(16,int(sys.argv[1])) # uncomment for fast testing
