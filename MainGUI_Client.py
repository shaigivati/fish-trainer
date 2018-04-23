#! /usr/bin/env python

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

import ConfigParser
import sys
import threading
import time
import subprocess
import multiprocessing
import os
import cv2
import numpy as np
from tracker.fish_tank import Tank
from tracker.tcp_client import FishClient
from tracker.controller import Controller
from tracker import track_fish
from tracker import scene_planner
from tools import fishlog

Config = ConfigParser.ConfigParser()
#Global vars
exit_var=False
stop_traning=False

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root, app
    root = Tk()
    app = GUIClass(root)
    #app.onRunTraining()

    #root.wm_attributes("-topmost", 1)
    root.focus_force()
    root.mainloop()

w = None

def create_Fish_traning_GUI_Client(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = Toplevel (root)
    top = Fish_traning_GUI___Client (w)
    ClientGUI_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_Fish_traning_GUI_Client():
    global w
    w.destroy()
    w = None


class GUIClass(Tk):
    #def __init__(self, top):
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#d9d9d9' # X11 color: 'gray85'
        font12 = "-family {TkDefaultFont} -size 20 " \
                 "-weight bold -slant roman -underline 0 -overstrike 0"
        font9 = "-family {.SF NS Text} -size 13 -weight normal -slant " \
                "roman -underline 0 -overstrike 0"

        top.geometry("793x800+292+31")
        top.title("Fish traning GUI - Client")
        top.configure(relief="raised")
        top.configure(background="#d9d9d9")

        self.frmTraining = Frame(top)
        self.frmTraining.place(relx=0.02, rely=0.53, relheight=0.1
                               , relwidth=0.96)
        self.frmTraining.configure(relief=GROOVE)
        self.frmTraining.configure(borderwidth="2")
        self.frmTraining.configure(relief=GROOVE)
        self.frmTraining.configure(background="#d9d9d9")
        self.frmTraining.configure(highlightbackground="#d9d9d9")
        self.frmTraining.configure(highlightcolor="black")
        self.frmTraining.configure(width=760)

        self.btnRunTraining = Button(self.frmTraining)
        self.btnRunTraining.place(relx=0.76, rely=0.1, height=64, width=89)
        self.btnRunTraining.configure(activebackground="#d9d9d9")
        self.btnRunTraining.configure(activeforeground="#000000")
        self.btnRunTraining.configure(background="#d9d9d9")
        self.btnRunTraining.configure(command=self.onRunTraining)
        self.btnRunTraining.configure(foreground="#000000")
        self.btnRunTraining.configure(highlightbackground="#d9d9d9")
        self.btnRunTraining.configure(highlightcolor="black")
        self.btnRunTraining.configure(text='''Run traning''')
        self.btnRunTraining.configure(width=89)

        self.txtFishNo = Text(self.frmTraining)
        self.txtFishNo.place(relx=0.01, rely=0.48, height=27, relwidth=0.12)
        self.txtFishNo.configure(background="white")
        self.txtFishNo.configure(font="TkFixedFont")
        self.txtFishNo.configure(foreground="#000000")
        self.txtFishNo.configure(highlightbackground="#d9d9d9")
        self.txtFishNo.configure(highlightcolor="black")
        self.txtFishNo.configure(insertbackground="black")
        self.txtFishNo.configure(selectbackground="#c4c4c4")
        self.txtFishNo.configure(selectforeground="black")

        self.Label2 = Label(self.frmTraining)
        self.Label2.place(relx=0.13, rely=0.1, height=24, width=85)
        self.Label2.configure(activebackground="#f9f9f9")
        self.Label2.configure(activeforeground="black")
        self.Label2.configure(background="#d9d9d9")
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(highlightbackground="#d9d9d9")
        self.Label2.configure(highlightcolor="black")
        self.Label2.configure(text='''Training day''')

        self.txtTrainingDay = Text(self.frmTraining)
        self.txtTrainingDay.place(relx=0.13, rely=0.48, height=27, relwidth=0.12)

        self.txtTrainingDay.configure(background="white")
        self.txtTrainingDay.configure(font="TkFixedFont")
        self.txtTrainingDay.configure(foreground="#000000")
        self.txtTrainingDay.configure(highlightbackground="#d9d9d9")
        self.txtTrainingDay.configure(highlightcolor="black")
        self.txtTrainingDay.configure(insertbackground="black")
        self.txtTrainingDay.configure(selectbackground="#c4c4c4")
        self.txtTrainingDay.configure(selectforeground="black")

        self.radF = Radiobutton(self.frmTraining)
        self.radF.place(relx=0.27, rely=0.19, relheight=0.27, relwidth=0.11)
        self.radF.configure(activebackground="#d9d9d9")
        self.radF.configure(activeforeground="#000000")
        self.radF.configure(background="#d9d9d9")
        self.radF.configure(foreground="#000000")
        self.radF.configure(highlightbackground="#d9d9d9")
        self.radF.configure(highlightcolor="black")
        self.radF.configure(justify=LEFT)
        self.radF.configure(text='''Feed''')

        self.radN = Radiobutton(self.frmTraining)
        self.radN.place(relx=0.27, rely=0.58, relheight=0.27, relwidth=0.13)
        self.radN.configure(activebackground="#d9d9d9")
        self.radN.configure(activeforeground="#000000")
        self.radN.configure(background="#d9d9d9")
        self.radN.configure(foreground="#000000")
        self.radN.configure(highlightbackground="#d9d9d9")
        self.radN.configure(highlightcolor="black")
        self.radN.configure(justify=LEFT)
        self.radN.configure(text='''No feed''')

        self.Label1 = Label(self.frmTraining)
        self.Label1.place(relx=0.01, rely=0.13, height=24, width=57)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(activeforeground="black")
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(highlightbackground="#d9d9d9")
        self.Label1.configure(highlightcolor="black")
        self.Label1.configure(text='''Fish no.''')

        self.txtArgs = Text(self.frmTraining)
        self.txtArgs.place(relx=0.39, rely=0.48, relheight=0.39, relwidth=0.35)
        self.txtArgs.configure(background="white")
        self.txtArgs.configure(font="TkTextFont")
        self.txtArgs.configure(foreground="black")
        self.txtArgs.configure(highlightbackground="#d9d9d9")
        self.txtArgs.configure(highlightcolor="black")
        self.txtArgs.configure(insertbackground="black")
        self.txtArgs.configure(selectbackground="#c4c4c4")
        self.txtArgs.configure(selectforeground="black")
        self.txtArgs.configure(undo="1")
        self.txtArgs.configure(width=266)
        self.txtArgs.configure(wrap=WORD)

        self.Label10 = Label(self.frmTraining)
        self.Label10.place(relx=0.39, rely=0.19, height=24, width=76)
        self.Label10.configure(activebackground="#f9f9f9")
        self.Label10.configure(activeforeground="black")
        self.Label10.configure(background="#d9d9d9")
        self.Label10.configure(foreground="#000000")
        self.Label10.configure(highlightbackground="#d9d9d9")
        self.Label10.configure(highlightcolor="black")
        self.Label10.configure(text='''Arguments''')

        self.btnStopTraning = Button(self.frmTraining)
        self.btnStopTraning.place(relx=0.88, rely=0.1, height=62, width=79)
        self.btnStopTraning.configure(activebackground="#d9d9d9")
        self.btnStopTraning.configure(activeforeground="#000000")
        self.btnStopTraning.configure(background="#d9d9d9")
        self.btnStopTraning.configure(foreground="#000000")
        self.btnStopTraning.configure(highlightbackground="#d9d9d9")
        self.btnStopTraning.configure(highlightcolor="black")
        self.btnStopTraning.configure(text='''Stop traning''')
        self.btnStopTraning.configure(command=self.onStopTraining)
        self.btnStopTraning.configure(width=79)

        self.btnExit = Button(top)
        self.btnExit.place(relx=0.74, rely=0.95, height=32, width=177)
        self.btnExit.configure(activebackground="#d9d9d9")
        self.btnExit.configure(activeforeground="#000000")
        self.btnExit.configure(background="#d9d9d9")
        self.btnExit.configure(command=self.onExit)
        self.btnExit.configure(foreground="#000000")
        self.btnExit.configure(highlightbackground="#d9d9d9")
        self.btnExit.configure(highlightcolor="black")
        self.btnExit.configure(text='''Exit''')
        self.btnExit.configure(width=177)

        self.frmStat = Frame(top)
        self.frmStat.place(relx=0.02, rely=0.01, relheight=0.38, relwidth=0.96)
        self.frmStat.configure(relief=GROOVE)
        self.frmStat.configure(borderwidth="2")
        self.frmStat.configure(relief=GROOVE)
        self.frmStat.configure(background="#d9d9d9")
        self.frmStat.configure(highlightbackground="#d9d9d9")
        self.frmStat.configure(highlightcolor="black")
        self.frmStat.configure(width=760)

        self.Label3 = Label(self.frmStat)
        self.Label3.place(relx=0.01, rely=0.03, height=24, width=96)
        self.Label3.configure(activebackground="#f9f9f9")
        self.Label3.configure(activeforeground="black")
        self.Label3.configure(background="#d9d9d9")
        self.Label3.configure(foreground="#000000")
        self.Label3.configure(highlightbackground="#d9d9d9")
        self.Label3.configure(highlightcolor="black")
        self.Label3.configure(text='''Fish statistics''')

        self.btnStatClear = Button(self.frmStat)
        self.btnStatClear.place(relx=0.01, rely=0.86, height=30, width=62)
        self.btnStatClear.configure(activebackground="#d9d9d9")
        self.btnStatClear.configure(activeforeground="#000000")
        self.btnStatClear.configure(background="#d9d9d9")
        self.btnStatClear.configure(command=self.onStatClear)
        self.btnStatClear.configure(foreground="#000000")
        self.btnStatClear.configure(highlightbackground="#d9d9d9")
        self.btnStatClear.configure(highlightcolor="black")
        self.btnStatClear.configure(text='''Clear''')

        self.btnStatRun = Button(self.frmStat)
        self.btnStatRun.place(relx=0.79, rely=0.83, height=22, width=141)
        self.btnStatRun.configure(activebackground="#d9d9d9")
        self.btnStatRun.configure(activeforeground="#000000")
        self.btnStatRun.configure(background="#d9d9d9")
        self.btnStatRun.configure(command=self.onStatRun)
        self.btnStatRun.configure(foreground="#000000")
        self.btnStatRun.configure(highlightbackground="#d9d9d9")
        self.btnStatRun.configure(highlightcolor="black")
        self.btnStatRun.configure(text='''Run''')
        self.btnStatRun.configure(width=141)

        self.txtLogFolder = Text(self.frmStat)
        self.txtLogFolder.place(relx=0.18, rely=0.1, height=27, relwidth=0.8)
        self.txtLogFolder.configure(background="white")
        self.txtLogFolder.configure(font="TkFixedFont")
        self.txtLogFolder.configure(foreground="#000000")
        self.txtLogFolder.configure(highlightbackground="#d9d9d9")
        self.txtLogFolder.configure(highlightcolor="black")
        self.txtLogFolder.configure(insertbackground="#000000")
        self.txtLogFolder.configure(selectbackground="#c4c4c4")
        self.txtLogFolder.configure(selectforeground="black")

        self.Label9 = Label(self.frmStat)
        self.Label9.place(relx=0.06, rely=0.1, height=24, width=89)
        self.Label9.configure(activebackground="#f9f9f9")
        self.Label9.configure(activeforeground="black")
        self.Label9.configure(background="#d9d9d9")
        self.Label9.configure(foreground="#000000")
        self.Label9.configure(highlightbackground="#d9d9d9")
        self.Label9.configure(highlightcolor="black")
        self.Label9.configure(text='''Log folder''')

        self.txtStatLog = Text(self.frmStat)
        self.txtStatLog.place(relx=0.01, rely=0.21, relheight=0.63
                              , relwidth=0.97)
        self.txtStatLog.configure(background="white")
        self.txtStatLog.configure(font="TkTextFont")
        self.txtStatLog.configure(foreground="black")
        self.txtStatLog.configure(highlightbackground="#d9d9d9")
        self.txtStatLog.configure(highlightcolor="black")
        self.txtStatLog.configure(insertbackground="black")
        self.txtStatLog.configure(selectbackground="#c4c4c4")
        self.txtStatLog.configure(selectforeground="black")
        self.txtStatLog.configure(undo="1")
        self.txtStatLog.configure(width=738)
        self.txtStatLog.configure(wrap=WORD)

        self.Label11 = Label(self.frmStat)
        self.Label11.place(relx=0.11, rely=0.83, height=24, width=73)
        self.Label11.configure(background="#d9d9d9")
        self.Label11.configure(foreground="#000000")
        self.Label11.configure(text='''Days back''')

        self.txtStatDaysBack = Text(self.frmStat)
        self.txtStatDaysBack.place(relx=0.21, rely=0.83, relheight=0.08
                                   , relwidth=0.09)
        self.txtStatDaysBack.configure(background="white")
        self.txtStatDaysBack.configure(foreground="black")
        self.txtStatDaysBack.configure(highlightbackground="#d9d9d9")
        self.txtStatDaysBack.configure(highlightcolor="black")
        self.txtStatDaysBack.configure(insertbackground="black")
        self.txtStatDaysBack.configure(selectbackground="#c4c4c4")
        self.txtStatDaysBack.configure(selectforeground="black")
        self.txtStatDaysBack.configure(undo="1")
        self.txtStatDaysBack.configure(width=66)
        self.txtStatDaysBack.configure(wrap=WORD)

        self.Label12 = Label(self.frmStat)
        self.Label12.place(relx=0.3, rely=0.83, height=24, width=33)
        self.Label12.configure(background="#d9d9d9")
        self.Label12.configure(foreground="#000000")
        self.Label12.configure(text='''Arg.''')

        self.txtStatArgs = Text(self.frmStat)
        self.txtStatArgs.place(relx=0.34, rely=0.83, relheight=0.08
                               , relwidth=0.1)
        self.txtStatArgs.configure(background="white")
        self.txtStatArgs.configure(foreground="black")
        self.txtStatArgs.configure(highlightbackground="#d9d9d9")
        self.txtStatArgs.configure(highlightcolor="black")
        self.txtStatArgs.configure(insertbackground="black")
        self.txtStatArgs.configure(selectbackground="#c4c4c4")
        self.txtStatArgs.configure(selectforeground="black")
        self.txtStatArgs.configure(undo="1")
        self.txtStatArgs.configure(width=74)
        self.txtStatArgs.configure(wrap=WORD)

        self.Label13 = Label(self.frmStat)
        self.Label13.place(relx=0.11, rely=0.91, height=24, width=60)
        self.Label13.configure(background="#d9d9d9")
        self.Label13.configure(foreground="#000000")
        self.Label13.configure(text='''Run arg.''')

        self.txtStatRunArgs = Text(self.frmStat)
        self.txtStatRunArgs.place(relx=0.21, rely=0.91, relheight=0.08
                                  , relwidth=0.76)
        self.txtStatRunArgs.configure(background="white")
        self.txtStatRunArgs.configure(foreground="black")
        self.txtStatRunArgs.configure(highlightbackground="#d9d9d9")
        self.txtStatRunArgs.configure(highlightcolor="black")
        self.txtStatRunArgs.configure(insertbackground="black")
        self.txtStatRunArgs.configure(selectbackground="#c4c4c4")
        self.txtStatRunArgs.configure(selectforeground="black")
        self.txtStatRunArgs.configure(undo="1")
        self.txtStatRunArgs.configure(width=578)
        self.txtStatRunArgs.configure(wrap=WORD)

        self.frmCom = Frame(top)
        self.frmCom.place(relx=0.02, rely=0.4, relheight=0.11, relwidth=0.96)
        self.frmCom.configure(relief=GROOVE)
        self.frmCom.configure(borderwidth="2")
        self.frmCom.configure(relief=GROOVE)
        self.frmCom.configure(background="#d9d9d9")
        self.frmCom.configure(width=760)

        self.Label4 = Label(self.frmCom)
        self.Label4.place(relx=0.01, rely=0.09, height=24, width=106)
        self.Label4.configure(background="#d9d9d9")
        self.Label4.configure(foreground="#000000")
        self.Label4.configure(text='''Communication''')

        self.txtServerIP = Entry(self.frmCom)
        self.txtServerIP.place(relx=0.03, rely=0.62,height=27, relwidth=0.2)
        self.txtServerIP.configure(background="white")
        self.txtServerIP.configure(font="TkFixedFont")
        self.txtServerIP.configure(foreground="#000000")
        self.txtServerIP.configure(insertbackground="black")

        self.Label5 = Label(self.frmCom)
        self.Label5.place(relx=0.03, rely=0.35, height=24, width=69)
        self.Label5.configure(background="#d9d9d9")
        self.Label5.configure(foreground="#000000")
        self.Label5.configure(text='''Server IP:''')

        self.btnComSend = Button(self.frmCom)
        self.btnComSend.place(relx=0.24, rely=0.09, height=70, width=86)
        self.btnComSend.configure(activebackground="#d9d9d9")
        self.btnComSend.configure(activeforeground="#000000")
        self.btnComSend.configure(background="#d9d9d9")
        self.btnComSend.configure(command=self.onSendtest)
        self.btnComSend.configure(foreground="#000000")
        self.btnComSend.configure(highlightbackground="#d9d9d9")
        self.btnComSend.configure(highlightcolor="black")
        self.btnComSend.configure(relief=RAISED)
        self.btnComSend.configure(text='''Send test''')
        self.btnComSend.configure(width=103)

        self.btnTankConfig = Button(self.frmCom)
        self.btnTankConfig.place(relx=0.36, rely=0.09, height=70, width=86)
        self.btnTankConfig.configure(activebackground="#d9d9d9")
        self.btnTankConfig.configure(activeforeground="#000000")
        self.btnTankConfig.configure(background="#d9d9d9")
        self.btnTankConfig.configure(command=self.onTankConfig)
        self.btnTankConfig.configure(foreground="#000000")
        self.btnTankConfig.configure(highlightbackground="#d9d9d9")
        self.btnTankConfig.configure(highlightcolor="black")
        self.btnTankConfig.configure(relief=RAISED)
        self.btnTankConfig.configure(text='''Tank conf.''')
        self.btnTankConfig.configure(width=103)

        self.Label6 = Label(self.frmCom)
        self.Label6.place(relx=0.53, rely=0.09, height=24, width=73)
        self.Label6.configure(background="#d9d9d9")
        self.Label6.configure(foreground="#000000")
        self.Label6.configure(text='''Motor test''')

        self.btnMotor1L = Button(self.frmCom)
        self.btnMotor1L.place(relx=0.71, rely=0.09, height=38, width=87)
        self.btnMotor1L.configure(activebackground="#d9d9d9")
        self.btnMotor1L.configure(activeforeground="#000000")
        self.btnMotor1L.configure(background="#d9d9d9")
        self.btnMotor1L.configure(command=self.on1L)
        self.btnMotor1L.configure(foreground="#000000")
        self.btnMotor1L.configure(highlightbackground="#d9d9d9")
        self.btnMotor1L.configure(highlightcolor="black")
        self.btnMotor1L.configure(relief=RAISED)
        self.btnMotor1L.configure(text='''(1) Left''')
        self.btnMotor1L.configure(width=87)

        self.btnMotor1R = Button(self.frmCom)
        self.btnMotor1R.place(relx=0.71, rely=0.53, height=38, width=87)
        self.btnMotor1R.configure(activebackground="#d9d9d9")
        self.btnMotor1R.configure(activeforeground="#000000")
        self.btnMotor1R.configure(background="#d9d9d9")
        self.btnMotor1R.configure(command=self.on1R)
        self.btnMotor1R.configure(foreground="#000000")
        self.btnMotor1R.configure(highlightbackground="#d9d9d9")
        self.btnMotor1R.configure(highlightcolor="black")
        self.btnMotor1R.configure(relief=RAISED)
        self.btnMotor1R.configure(text='''(1) Right''')
        self.btnMotor1R.configure(width=87)

        self.btnMotor2R = Button(self.frmCom)
        self.btnMotor2R.place(relx=0.86, rely=0.53, height=38, width=87)
        self.btnMotor2R.configure(activebackground="#d9d9d9")
        self.btnMotor2R.configure(activeforeground="#000000")
        self.btnMotor2R.configure(background="#d9d9d9")
        self.btnMotor2R.configure(command=self.on2R)
        self.btnMotor2R.configure(foreground="#000000")
        self.btnMotor2R.configure(highlightbackground="#d9d9d9")
        self.btnMotor2R.configure(highlightcolor="black")
        self.btnMotor2R.configure(relief=RAISED)
        self.btnMotor2R.configure(text='''(2) Right''')
        self.btnMotor2R.configure(width=87)

        self.btnMotor2L = Button(self.frmCom)
        self.btnMotor2L.place(relx=0.86, rely=0.09, height=38, width=87)
        self.btnMotor2L.configure(activebackground="#d9d9d9")
        self.btnMotor2L.configure(activeforeground="#000000")
        self.btnMotor2L.configure(background="#d9d9d9")
        self.btnMotor2L.configure(command=self.on2L)
        self.btnMotor2L.configure(foreground="#000000")
        self.btnMotor2L.configure(highlightbackground="#d9d9d9")
        self.btnMotor2L.configure(highlightcolor="black")
        self.btnMotor2L.configure(relief=RAISED)
        self.btnMotor2L.configure(text='''(2) Left''')
        self.btnMotor2L.configure(width=87)

        self.Label7 = Label(self.frmCom)
        self.Label7.place(relx=0.55, rely=0.35, height=24, width=96)
        self.Label7.configure(background="#d9d9d9")
        self.Label7.configure(foreground="#000000")
        self.Label7.configure(text='''Steps number''')

        self.txtStepNum = Entry(self.frmCom)
        self.txtStepNum.place(relx=0.57, rely=0.62,height=27, relwidth=0.11)
        self.txtStepNum.configure(background="white")
        self.txtStepNum.configure(font="TkFixedFont")
        self.txtStepNum.configure(foreground="#000000")
        self.txtStepNum.configure(insertbackground="black")
        self.txtStepNum.configure(width=80)

        self.frmLog = Frame(top)
        self.frmLog.place(relx=0.02, rely=0.65, relheight=0.29, relwidth=0.95)
        self.frmLog.configure(relief=GROOVE)
        self.frmLog.configure(borderwidth="2")
        self.frmLog.configure(relief=GROOVE)
        self.frmLog.configure(background="#d9d9d9")
        self.frmLog.configure(width=757)

        self.Label8 = Label(self.frmLog)
        self.Label8.place(relx=0.01, rely=0.03, height=24, width=30)
        self.Label8.configure(background="#d9d9d9")
        self.Label8.configure(foreground="#000000")
        self.Label8.configure(text='''Log''')

        self.txtMainLog = Text(self.frmLog)
        self.txtMainLog.place(relx=0.01, rely=0.14, relheight=0.75
                              , relwidth=0.97)
        self.txtMainLog.configure(background="white")
        self.txtMainLog.configure(font="TkTextFont")
        self.txtMainLog.configure(foreground="black")
        self.txtMainLog.configure(highlightbackground="#d9d9d9")
        self.txtMainLog.configure(highlightcolor="black")
        self.txtMainLog.configure(insertbackground="black")
        self.txtMainLog.configure(selectbackground="#c4c4c4")
        self.txtMainLog.configure(selectforeground="black")
        self.txtMainLog.configure(undo="1")
        self.txtMainLog.configure(width=738)
        self.txtMainLog.configure(wrap=WORD)

        self.frmLogClear = Button(self.frmLog)
        self.frmLogClear.place(relx=0.01, rely=0.89, height=22, width=70)
        self.frmLogClear.configure(activebackground="#d9d9d9")
        self.frmLogClear.configure(activeforeground="#000000")
        self.frmLogClear.configure(background="#d9d9d9")
        self.frmLogClear.configure(command=self.onLogClear)
        self.frmLogClear.configure(foreground="#000000")
        self.frmLogClear.configure(highlightbackground="#d9d9d9")
        self.frmLogClear.configure(highlightcolor="black")
        self.frmLogClear.configure(text='''Clear''')
        self.frmLogClear.configure(width=70)

        self.Label14 = Label(self.frmLog)
        self.Label14.place(relx=0.15, rely=0.03, height=24, width=87)
        self.Label14.configure(background="#d9d9d9")
        self.Label14.configure(foreground="#000000")
        self.Label14.configure(text='''Time runing:''')

        self.str_time = StringVar()

        self.Label15 = Label(self.frmLog)
        self.Label15.place(relx=0.27, rely=0.03, height=24, width=209)
        self.Label15.configure(background="#d9d9d9")
        self.Label15.configure(font=font12)
        self.Label15.configure(foreground="#0000fe")
        self.Label15.configure(text='__:__')
        self.Label15.configure(width=209)
        self.Label15.configure(textvariable=self.str_time)


        self.fillValue()

    def fillValue(self):
        Config.read('GUI_config.txt')
        self.LogFolderName = ConfigSectionMap("Fish Statistics")['log folder']
        self.Stat_days = ConfigSectionMap("Fish Statistics")['days back']
        self.Stat_arg = ConfigSectionMap("Fish Statistics")['arg']

        ServerIP = ConfigSectionMap("Communication")['server ip']
        Arg1 = ConfigSectionMap("Fish")['argument1']
        Arg2 = ConfigSectionMap("Fish")['argument2']
        Args = '{} {}'.format(Arg1, Arg2)

        #print Args

        self.txtLogFolder.insert('0.0', self.LogFolderName)
        self.txtServerIP.insert('0', ServerIP)
        self.txtArgs.insert('0.0', Args)
        self.txtStatDaysBack.insert('0.0', self.Stat_days)
        self.txtStatArgs.insert('0.0', self.Stat_arg)
        temp_run_arg = "{} {} {} {}".format('fish_stat.py', self.LogFolderName, self.Stat_days, self.Stat_arg)
        self.txtStatRunArgs.insert('0.0', temp_run_arg)

    def Feed(self):
        print('ClientGUI_support.Feed')
        sys.stdout.flush()

    def on1L(self):
        print('ClientGUI_support.on1L')
        sys.stdout.flush()

    def on1R(self):
        print('ClientGUI_support.on1R')
        sys.stdout.flush()

    def on2L(self):
        print('ClientGUI_support.on2L')
        sys.stdout.flush()

    def on2R(self):
        print('ClientGUI_support.on2R')
        sys.stdout.flush()

    def onExit(self):
        global exit_var
        print('ClientGUI_support.onExit')
        sys.stdout.flush()

        exit_var=True
        sys.exit(1)

    def onStopTraining(self):
        global stop_traning
        sys.stdout.flush()
        stop_traning=True
        app.txtMainLog.insert(END, 'Stopped!')

    def onRunTraining(self):

        global stop_traning
        sys.stdout.flush()

        stop_traning=False
        log_name=[]
        log_name.append('F{}DAY{}'.format(app.txtFishNo.get('0.0', 'end-1c'), app.txtTrainingDay.get('0.0', 'end-1c')))

        controller = Controller(app, log_name)
        thread_track_fish = threading.Thread(target=track_fish.track_loop, args=(controller,))

        thread_track_fish.daemon=True
        thread_track_fish.start()

        #tf_sub = subprocess.Popen(track_fish('tank_config.txt', 'F9DAY2'))


    def onSendtest(self):
        print('ClientGUI_support.onSendtest')
        sys.stdout.flush()
        fish_client = FishClient()
        fish_client.send('test', 0)
        fish_client.kill()

    def onTankConfig(self):
        print('ClientGUI_support.onTankConfig')
        sys.stdout.flush()
        thread_track_fish = threading.Thread(target=scene_planner.SP_Main, args=())
        thread_track_fish.start()



    def onStatClear(self):
        sys.stdout.flush()
        app.txtStatLog.delete('0.0',END)

    def onLogClear(self):
        sys.stdout.flush()
        app.txtMainLog.delete('0.0',END)

    def onStatRun(self):
        sys.stdout.flush()
        StatInfo = ThreadingProcess('fish_stat.py', self.LogFolderName, self.txtStatDaysBack.get('0.0', END), self.txtStatArgs.get('0.0', END)).run()
        app.txtStatLog.insert(END, StatInfo)
        app.txtStatLog.see(END)
        #print "HERE:{}".format(StatInfo)

    def print_and_update_main_log(self, str_to_print, new_line=True):
        str_temp = '{}'.format(str_to_print)
        print (str_temp)
        if new_line: str_temp = '{}\n'.format(str_temp)
        app.txtMainLog.insert(END, str_temp)
        app.txtMainLog.see(END)

    def __call__(self):
        print "RUN Command"


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



def make_two_digit_num(int_to_check):
    str_temp='{}'.format(int_to_check)
    if int_to_check<10: str_temp='0{}'.format(int_to_check)
    return str_temp

if __name__ == '__main__':
    vp_start_gui()

