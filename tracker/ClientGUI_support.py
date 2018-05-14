#! /usr/bin/env python
#
# Support module generated by PAGE version 4.10
# In conjunction with Tcl version 8.6
#    Feb 24, 2018 06:27:58 PM
#    Apr 23, 2018 08:54:50 PM

thread_track_fish = None

import sys
import subprocess
import threading
from tracker import scene_planner
from tracker.controller import Controller
from tracker import track_fish
from tracker.tcp_client import FishClient



try:
    from Tkinter import *
except ImportError:
    from tkinter import *

try:
    import ttk
    py3 = 0
except ImportError:
    import tkinter.ttk as ttk
    py3 = 1


def set_Tk_var():
    global FeedVar
    FeedVar = StringVar()

def onLogClear():
    sys.stdout.flush()
    w.txtMainLog.delete('0.0',END)


def Feed():
    print('ClientGUI_support.Feed')
    sys.stdout.flush()

def on1L():
    print('ClientGUI_support.on1L')
    fish_client = FishClient()
    fish_client.send('test_1L', w.txtStepNum.get())
    fish_client.kill()
    sys.stdout.flush()

def on1R():
    print('ClientGUI_support.on1R')
    fish_client = FishClient()
    fish_client.send('test_1R', w.txtStepNum.get())
    fish_client.kill()
    sys.stdout.flush()

def on2L():
    print('ClientGUI_support.on2L')

    fish_client = FishClient()
    fish_client.send('test_2L', w.txtStepNum.get())
    fish_client.kill()

    sys.stdout.flush()

def on2R():
    print('ClientGUI_support.on2R')
    fish_client = FishClient()
    fish_client.send('test_2R', w.txtStepNum.get())
    fish_client.kill()
    sys.stdout.flush()

def onExit():
    global exit_var
    print('ClientGUI_support.onExit')
    sys.stdout.flush()
    onStopTraining()
    exit_var = True
    sys.exit(1)

def onRunTraining():
    global stop_traning, thread_track_fish
    sys.stdout.flush()

    stop_traning = False
    log_name = []
    log_name.append('F{}DAY{}'.format(w.txtFishNo1.get('0.0', 'end-1c'), w.txtTrainingDay1.get('0.0', 'end-1c')))

    controller = Controller(w, log_name)

    thread_track_fish = threading.Thread(target=track_fish.track_loop, args=(controller,))

    thread_track_fish.daemon = True
    #print('thread_track_fish:{0}'.format(thread_track_fish))
    thread_track_fish.start()
    #print('thread_track_fish:{0}'.format(thread_track_fish))



def onStopTraining():
    global stop_traning, w, thread_track_fish
    sys.stdout.flush()
    if track_fish.stop_training==False:
        track_fish.stop_training=True
    else:
        track_fish.stop_training=False

    w.print_and_update_main_log("Stopped!")
    w.print_and_update_main_log(track_fish.stop_training)
    #print('thread_track_fish:{0}'.format(thread_track_fish))
    if thread_track_fish==None:
        print 'No thread'
    else:
        print thread_track_fish
        thread_track_fish.join()

    #print('thread_track_fish:{0}'.format(thread_track_fish))

def onSendtest():
    print('ClientGUI_support.onSendtest')
    sys.stdout.flush()
    fish_client = FishClient()
    fish_client.send('test_com', 0)
    fish_client.kill()

def onStatClear():
    sys.stdout.flush()
    w.txtStatLog.delete('0.0', END)

def onTankConfig():
        print('ClientGUI_support.onTankConfig')
        sys.stdout.flush()
        thread_track_fish = threading.Thread(target=scene_planner.SP_Main, args=())
        thread_track_fish.start()

def onStatRun():
    global w
    sys.stdout.flush()
    _StatInfo = ThreadingProcess('fish_stat.py', w.LogFolderName, w.txtStatDaysBack.get('0.0', END),
    w.txtStatArgs.get('0.0', END)).run()
    w.txtStatLog.insert(END, _StatInfo)
    w.txtStatLog.see(END)
    # print "HERE:{}".format(StatInfo)

def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top

def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None

class ThreadingProcess(object):

    def __init__(self, file_name, arg0='', arg1='', arg2=''):
        self.interval = 1
        self.file_name = file_name
        self.arg0 = arg0
        self.arg1 = arg1
        self.arg2 = arg2

        #thread = threading.Thread(target=self.run(), args=args)
        #thread.daemon = True                            # Daemonize thread
        #thread.start()                                  # Start the execution


    def runTrack(self, process):
        try:

            str_name = [sys.executable, self.file_name, self.arg0, self.arg1, self.arg2]
            process = subprocess.Popen(str_name, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error_output = process.communicate()
            print(process.stdout.readline())
        except:
            print 'Err - Check (.py) call file'
            if output=='': output=error_output

        #return output

    def run(self):
        #print self.file_name
        #while True:
        #    print('Doing something imporant in the background')
        #file = '/Users/talzoor/PycharmProjects/test/fish_stat.py'
        try:
            process = subprocess.Popen(['python', self.file_name, self.arg0, self.arg1, self.arg2], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error_output = process.communicate()

        except:
            print 'Err - Check (fish_stat.py) call file'

        if output=='': output=error_output
        return output


class Counter(object):
    def __init__(self, start=0):
        self.lock = threading.Lock()
        self.value = start

    def increment(self):
        logging.debug('Waiting for a lock')
        self.lock.acquire()
        try:
            logging.debug('Acquired a lock')
            self.value = self.value + 1
        finally:
            logging.debug('Released a lock')
            self.lock.release()



if __name__ == '__main__':
    import ClientGUI
    ClientGUI.vp_start_gui()





