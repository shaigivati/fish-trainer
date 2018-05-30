#!/usr/bin/env python

import socket
import json


class FishClient:

    def __init__(self, cb_obj=None):
        self.TCP_IP = '132.72.91.148' # self.TCP_IP = '132.72.44.66' # self.TCP_IP = '132.73.194.80'

        self.TCP_PORT = 50007
        self.BUFFER_SIZE = 1024
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.TCP_IP, self.TCP_PORT))

        self.cb_obj = cb_obj

    def send(self, id_num, side, steps=None, velocity=None, accl=None):
        if velocity is None:
            data = json.dumps({'id': id_num, 'side': side})
        else:
            data = json.dumps({'id': id_num, 'side': side, 'steps': steps, 'velocity': velocity, 'accl': accl})

        self.s.send(data)
        old_data = data
        # print('DATA_SENT:{}'.format(data))
        data = self.s.recv(self.BUFFER_SIZE)
        # print('DATA_REC:{}'.format(data))
        # print ('ECHO OK? {}'.format(old_data == data))

        if old_data == data:
            str_to_print = 'echo OK. \t\t'
        else:
            str_to_print = 'ERROR! CHECK CONNECTION!'
        if self.cb_obj is not None:
            self.cb_obj.print_and_update_main_log(str_to_print, False)
        # print (str_to_print)

    def kill(self):
        self.s.close()
