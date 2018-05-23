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
import time
import multiprocessing
import os
import cv2
import numpy as np
from tracker.fish_tank import Tank

from tools import fishlog
from tracker import ClientGUI_support

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
    global val, w, root
    root = Tk()
    ClientGUI_support.set_Tk_var()
    top = Fish_traning_GUI___Client (root)
    ClientGUI_support.init(root, top)
    root.mainloop()

w = None
def create_Fish_traning_GUI___Client(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = Toplevel (root)
    ClientGUI_support.set_Tk_var()
    top = Fish_traning_GUI___Client (w)
    ClientGUI_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_Fish_traning_GUI___Client():
    global w
    w.destroy()
    w = None




class Fish_traning_GUI___Client:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#d9d9d9' # X11 color: 'gray85'
        font12 = "-family {Abadi MT Condensed Extra Bold} -size 20 "  \
            "-weight bold -slant roman -underline 0 -overstrike 0"
        font9 = "-family {.SF NS Text} -size 13 -weight normal -slant "  \
            "roman -underline 0 -overstrike 0"

        top.geometry("891x800+281+53")
        top.title("Fish traning GUI - Client")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")



        self.frmTraining = Frame(top)
        self.frmTraining.place(relx=0.01, rely=0.47, relheight=0.16
                , relwidth=0.97)
        self.frmTraining.configure(relief=GROOVE)
        self.frmTraining.configure(borderwidth="2")
        self.frmTraining.configure(relief=GROOVE)
        self.frmTraining.configure(background="#d9d9d9")
        self.frmTraining.configure(highlightbackground="#d9d9d9")
        self.frmTraining.configure(highlightcolor="black")
        self.frmTraining.configure(width=864)

        self.btnRunTraining = Button(self.frmTraining)
        self.btnRunTraining.place(relx=0.78, rely=0.43, height=64, width=89)
        self.btnRunTraining.configure(activebackground="#d9d9d9")
        self.btnRunTraining.configure(activeforeground="#000000")
        self.btnRunTraining.configure(background="#d9d9d9")
        self.btnRunTraining.configure(command=ClientGUI_support.onRunTraining)
        self.btnRunTraining.configure(foreground="#000000")
        self.btnRunTraining.configure(highlightbackground="#d9d9d9")
        self.btnRunTraining.configure(highlightcolor="black")
        self.btnRunTraining.configure(text='''Run traning''')

        self.Label2 = Label(self.frmTraining)
        self.Label2.place(relx=0.12, rely=0.06, height=24, width=85)
        self.Label2.configure(activebackground="#f9f9f9")
        self.Label2.configure(activeforeground="black")
        self.Label2.configure(background="#d9d9d9")
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(highlightbackground="#d9d9d9")
        self.Label2.configure(highlightcolor="black")
        self.Label2.configure(text='''Training day''')

        self.radF1 = Radiobutton(self.frmTraining)
        self.radF1.place(relx=0.24, rely=0.12, relheight=0.17, relwidth=0.09)
        self.radF1.configure(activebackground="#d9d9d9")
        self.radF1.configure(activeforeground="#000000")
        self.radF1.configure(background="#d9d9d9")
        self.radF1.configure(foreground="#000000")
        self.radF1.configure(highlightbackground="#d9d9d9")
        self.radF1.configure(highlightcolor="black")
        self.radF1.configure(justify=LEFT)
        self.radF1.configure(text='''Feed''')
        self.radF1.configure(variable=ClientGUI_support.FeedVar)

        self.radN1 = Radiobutton(self.frmTraining)
        self.radN1.place(relx=0.24, rely=0.31, relheight=0.17, relwidth=0.11)
        self.radN1.configure(activebackground="#d9d9d9")
        self.radN1.configure(activeforeground="#000000")
        self.radN1.configure(background="#d9d9d9")
        self.radN1.configure(foreground="#000000")
        self.radN1.configure(highlightbackground="#d9d9d9")
        self.radN1.configure(highlightcolor="black")
        self.radN1.configure(justify=LEFT)
        self.radN1.configure(text='''No feed''')
        self.radN1.configure(variable=ClientGUI_support.FeedVar)

        self.Label1 = Label(self.frmTraining)
        self.Label1.place(relx=0.01, rely=0.06, height=24, width=57)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(activeforeground="black")
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(highlightbackground="#d9d9d9")
        self.Label1.configure(highlightcolor="black")
        self.Label1.configure(text='''Fish no.''')

        self.txtArgs = Text(self.frmTraining)
        self.txtArgs.place(relx=0.52, rely=0.67, relheight=0.24, relwidth=0.25)
        self.txtArgs.configure(background="white")
        self.txtArgs.configure(font="TkTextFont")
        self.txtArgs.configure(foreground="black")
        self.txtArgs.configure(highlightbackground="#d9d9d9")
        self.txtArgs.configure(highlightcolor="black")
        self.txtArgs.configure(insertbackground="black")
        self.txtArgs.configure(selectbackground="#c4c4c4")
        self.txtArgs.configure(selectforeground="black")
        self.txtArgs.configure(undo="1")
        self.txtArgs.configure(width=218)
        self.txtArgs.configure(wrap=WORD)

        self.Label10 = Label(self.frmTraining)
        self.Label10.place(relx=0.52, rely=0.43, height=24, width=76)
        self.Label10.configure(activebackground="#f9f9f9")
        self.Label10.configure(activeforeground="black")
        self.Label10.configure(background="#d9d9d9")
        self.Label10.configure(foreground="#000000")
        self.Label10.configure(highlightbackground="#d9d9d9")
        self.Label10.configure(highlightcolor="black")
        self.Label10.configure(text='''Arguments''')

        self.btnStopTraning = Button(self.frmTraining)
        self.btnStopTraning.place(relx=0.89, rely=0.43, height=62, width=87)
        self.btnStopTraning.configure(activebackground="#d9d9d9")
        self.btnStopTraning.configure(activeforeground="#000000")
        self.btnStopTraning.configure(background="#d9d9d9")
        self.btnStopTraning.configure(command=ClientGUI_support.onStopTraining)
        self.btnStopTraning.configure(foreground="#000000")
        self.btnStopTraning.configure(highlightbackground="#d9d9d9")
        self.btnStopTraning.configure(highlightcolor="black")
        self.btnStopTraning.configure(text='''Stop traning''')

        self.txtFishNo1 = Text(self.frmTraining)
        self.txtFishNo1.place(relx=0.02, rely=0.24, relheight=0.24, relwidth=0.1)

        self.txtFishNo1.configure(background="white")
        self.txtFishNo1.configure(font=font9)
        self.txtFishNo1.configure(foreground="black")
        self.txtFishNo1.configure(highlightbackground="#d9d9d9")
        self.txtFishNo1.configure(highlightcolor="black")
        self.txtFishNo1.configure(insertbackground="black")
        self.txtFishNo1.configure(selectbackground="#c4c4c4")
        self.txtFishNo1.configure(selectforeground="black")
        self.txtFishNo1.configure(undo="1")
        self.txtFishNo1.configure(width=90)
        self.txtFishNo1.configure(wrap=WORD)

        self.txtTrainingDay1 = Text(self.frmTraining)
        self.txtTrainingDay1.place(relx=0.14, rely=0.24, relheight=0.24
                , relwidth=0.09)
        self.txtTrainingDay1.configure(background="white")
        self.txtTrainingDay1.configure(font=font9)
        self.txtTrainingDay1.configure(foreground="black")
        self.txtTrainingDay1.configure(highlightbackground="#d9d9d9")
        self.txtTrainingDay1.configure(highlightcolor="black")
        self.txtTrainingDay1.configure(insertbackground="black")
        self.txtTrainingDay1.configure(selectbackground="#c4c4c4")
        self.txtTrainingDay1.configure(selectforeground="black")
        self.txtTrainingDay1.configure(undo="1")
        self.txtTrainingDay1.configure(width=82)
        self.txtTrainingDay1.configure(wrap=WORD)

        self.txtFishNo2 = Text(self.frmTraining)
        self.txtFishNo2.place(relx=0.02, rely=0.55, relheight=0.24, relwidth=0.1)

        self.txtFishNo2.configure(background="white")
        self.txtFishNo2.configure(font=font9)
        self.txtFishNo2.configure(foreground="black")
        self.txtFishNo2.configure(highlightbackground="#d9d9d9")
        self.txtFishNo2.configure(highlightcolor="black")
        self.txtFishNo2.configure(insertbackground="black")
        self.txtFishNo2.configure(selectbackground="#c4c4c4")
        self.txtFishNo2.configure(selectforeground="black")
        self.txtFishNo2.configure(undo="1")
        self.txtFishNo2.configure(width=90)
        self.txtFishNo2.configure(wrap=WORD)

        self.txtTrainingDay2 = Text(self.frmTraining)
        self.txtTrainingDay2.place(relx=0.14, rely=0.55, relheight=0.24
                , relwidth=0.09)
        self.txtTrainingDay2.configure(background="white")
        self.txtTrainingDay2.configure(font=font9)
        self.txtTrainingDay2.configure(foreground="black")
        self.txtTrainingDay2.configure(highlightbackground="#d9d9d9")
        self.txtTrainingDay2.configure(highlightcolor="black")
        self.txtTrainingDay2.configure(insertbackground="black")
        self.txtTrainingDay2.configure(selectbackground="#c4c4c4")
        self.txtTrainingDay2.configure(selectforeground="black")
        self.txtTrainingDay2.configure(undo="1")
        self.txtTrainingDay2.configure(width=82)
        self.txtTrainingDay2.configure(wrap=WORD)

        self.radF2 = Radiobutton(self.frmTraining)
        self.radF2.place(relx=0.24, rely=0.49, relheight=0.17, relwidth=0.06)
        self.radF2.configure(activebackground="#d9d9d9")
        self.radF2.configure(activeforeground="#000000")
        self.radF2.configure(background="#d9d9d9")
        self.radF2.configure(foreground="#000000")
        self.radF2.configure(highlightbackground="#d9d9d9")
        self.radF2.configure(highlightcolor="black")
        self.radF2.configure(justify=LEFT)
        self.radF2.configure(text='''Feed''')

        self.radN2 = Radiobutton(self.frmTraining)
        self.radN2.place(relx=0.24, rely=0.67, relheight=0.17, relwidth=0.09)
        self.radN2.configure(activebackground="#d9d9d9")
        self.radN2.configure(activeforeground="#000000")
        self.radN2.configure(background="#d9d9d9")
        self.radN2.configure(foreground="#000000")
        self.radN2.configure(highlightbackground="#d9d9d9")
        self.radN2.configure(highlightcolor="black")
        self.radN2.configure(justify=LEFT)
        self.radN2.configure(text='''No feed''')

        self.btnExit = Button(top)
        self.btnExit.place(relx=0.78, rely=0.94, height=40, width=177)
        self.btnExit.configure(activebackground="#d9d9d9")
        self.btnExit.configure(activeforeground="#000000")
        self.btnExit.configure(background="#d9d9d9")
        self.btnExit.configure(command=ClientGUI_support.onExit)
        self.btnExit.configure(foreground="#000000")
        self.btnExit.configure(highlightbackground="#d9d9d9")
        self.btnExit.configure(highlightcolor="black")
        self.btnExit.configure(text='''Exit''')


        self.frmStat = Frame(top)
        self.frmStat.place(relx=0.02, rely=0.01, relheight=0.33, relwidth=0.97)
        self.frmStat.configure(relief=GROOVE)
        self.frmStat.configure(borderwidth="2")
        self.frmStat.configure(relief=GROOVE)
        self.frmStat.configure(background="#d9d9d9")
        self.frmStat.configure(highlightbackground="#d9d9d9")
        self.frmStat.configure(highlightcolor="black")
        self.frmStat.configure(width=864)

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
        self.btnStatClear.place(relx=0.01, rely=0.84, height=30, width=62)
        self.btnStatClear.configure(activebackground="#d9d9d9")
        self.btnStatClear.configure(activeforeground="#000000")
        self.btnStatClear.configure(background="#d9d9d9")
        self.btnStatClear.configure(command=ClientGUI_support.onStatClear)
        self.btnStatClear.configure(foreground="#000000")
        self.btnStatClear.configure(highlightbackground="#d9d9d9")
        self.btnStatClear.configure(highlightcolor="black")
        self.btnStatClear.configure(text='''Clear''')

        self.btnStatRun = Button(self.frmStat)
        self.btnStatRun.place(relx=0.81, rely=0.81, height=38, width=141)
        self.btnStatRun.configure(activebackground="#d9d9d9")
        self.btnStatRun.configure(activeforeground="#000000")
        self.btnStatRun.configure(background="#d9d9d9")
        self.btnStatRun.configure(command=ClientGUI_support.onStatRun)
        self.btnStatRun.configure(foreground="#000000")
        self.btnStatRun.configure(highlightbackground="#d9d9d9")
        self.btnStatRun.configure(highlightcolor="black")
        self.btnStatRun.configure(text='''Run''')

        self.Label9 = Label(self.frmStat)
        self.Label9.place(relx=0.36, rely=0.03, height=24, width=89)
        self.Label9.configure(activebackground="#f9f9f9")
        self.Label9.configure(activeforeground="black")
        self.Label9.configure(background="#d9d9d9")
        self.Label9.configure(foreground="#000000")
        self.Label9.configure(highlightbackground="#d9d9d9")
        self.Label9.configure(highlightcolor="black")
        self.Label9.configure(text='''Log folder''')

        self.txtStatLog = Text(self.frmStat)
        self.txtStatLog.place(relx=0.01, rely=0.15, relheight=0.63
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
        self.txtStatLog.configure(width=842)
        self.txtStatLog.configure(wrap=WORD)

        self.Label11 = Label(self.frmStat)
        self.Label11.place(relx=0.09, rely=0.81, height=24, width=73)
        self.Label11.configure(activebackground="#f9f9f9")
        self.Label11.configure(activeforeground="black")
        self.Label11.configure(background="#d9d9d9")
        self.Label11.configure(foreground="#000000")
        self.Label11.configure(highlightbackground="#d9d9d9")
        self.Label11.configure(highlightcolor="black")
        self.Label11.configure(text='''Days back''')

        self.txtStatDaysBack = Text(self.frmStat)
        self.txtStatDaysBack.place(relx=0.19, rely=0.81, relheight=0.09
                , relwidth=0.08)
        self.txtStatDaysBack.configure(background="white")
        self.txtStatDaysBack.configure(font=font9)
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
        self.Label12.place(relx=0.28, rely=0.81, height=24, width=33)
        self.Label12.configure(activebackground="#f9f9f9")
        self.Label12.configure(activeforeground="black")
        self.Label12.configure(background="#d9d9d9")
        self.Label12.configure(foreground="#000000")
        self.Label12.configure(highlightbackground="#d9d9d9")
        self.Label12.configure(highlightcolor="black")
        self.Label12.configure(text='''Arg.''')

        self.txtStatArgs = Text(self.frmStat)
        self.txtStatArgs.place(relx=0.33, rely=0.81, relheight=0.09
                , relwidth=0.09)
        self.txtStatArgs.configure(background="white")
        self.txtStatArgs.configure(font=font9)
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
        self.Label13.place(relx=0.09, rely=0.9, height=24, width=60)
        self.Label13.configure(activebackground="#f9f9f9")
        self.Label13.configure(activeforeground="black")
        self.Label13.configure(background="#d9d9d9")
        self.Label13.configure(foreground="#000000")
        self.Label13.configure(highlightbackground="#d9d9d9")
        self.Label13.configure(highlightcolor="black")
        self.Label13.configure(text='''Run arg.''')

        self.txtStatRunArgs = Text(self.frmStat)
        self.txtStatRunArgs.place(relx=0.19, rely=0.9, relheight=0.09
                , relwidth=0.44)
        self.txtStatRunArgs.configure(background="white")
        self.txtStatRunArgs.configure(font=font9)
        self.txtStatRunArgs.configure(foreground="black")
        self.txtStatRunArgs.configure(highlightbackground="#d9d9d9")
        self.txtStatRunArgs.configure(highlightcolor="black")
        self.txtStatRunArgs.configure(insertbackground="black")
        self.txtStatRunArgs.configure(selectbackground="#c4c4c4")
        self.txtStatRunArgs.configure(selectforeground="black")
        self.txtStatRunArgs.configure(undo="1")
        self.txtStatRunArgs.configure(width=378)
        self.txtStatRunArgs.configure(wrap=WORD)

        self.txtLogFolder = Text(self.frmStat)
        self.txtLogFolder.place(relx=0.46, rely=0.03, relheight=0.09
                , relwidth=0.51)
        self.txtLogFolder.configure(background="white")
        self.txtLogFolder.configure(font=font9)
        self.txtLogFolder.configure(foreground="black")
        self.txtLogFolder.configure(highlightbackground="#d9d9d9")
        self.txtLogFolder.configure(highlightcolor="black")
        self.txtLogFolder.configure(insertbackground="black")
        self.txtLogFolder.configure(selectbackground="#c4c4c4")
        self.txtLogFolder.configure(selectforeground="black")
        self.txtLogFolder.configure(undo="1")
        self.txtLogFolder.configure(width=442)
        self.txtLogFolder.configure(wrap=WORD)

        self.frmCom = Frame(top)
        self.frmCom.place(relx=0.02, rely=0.35, relheight=0.11, relwidth=0.97)
        self.frmCom.configure(relief=GROOVE)
        self.frmCom.configure(borderwidth="2")
        self.frmCom.configure(relief=GROOVE)
        self.frmCom.configure(background="#d9d9d9")
        self.frmCom.configure(highlightbackground="#d9d9d9")
        self.frmCom.configure(highlightcolor="black")
        self.frmCom.configure(width=864)

        self.Label4 = Label(self.frmCom)
        self.Label4.place(relx=0.01, rely=0.09, height=24, width=106)
        self.Label4.configure(activebackground="#f9f9f9")
        self.Label4.configure(activeforeground="black")
        self.Label4.configure(background="#d9d9d9")
        self.Label4.configure(foreground="#000000")
        self.Label4.configure(highlightbackground="#d9d9d9")
        self.Label4.configure(highlightcolor="black")
        self.Label4.configure(text='''Communication''')

        self.txtServerIP = Entry(self.frmCom)
        self.txtServerIP.place(relx=0.02, rely=0.62,height=27, relwidth=0.18)
        self.txtServerIP.configure(background="white")
        self.txtServerIP.configure(font="TkFixedFont")
        self.txtServerIP.configure(foreground="#000000")
        self.txtServerIP.configure(highlightbackground="#d9d9d9")
        self.txtServerIP.configure(highlightcolor="black")
        self.txtServerIP.configure(insertbackground="black")
        self.txtServerIP.configure(selectbackground="#c4c4c4")
        self.txtServerIP.configure(selectforeground="black")

        self.Label5 = Label(self.frmCom)
        self.Label5.place(relx=0.02, rely=0.35, height=24, width=69)
        self.Label5.configure(activebackground="#f9f9f9")
        self.Label5.configure(activeforeground="black")
        self.Label5.configure(background="#d9d9d9")
        self.Label5.configure(foreground="#000000")
        self.Label5.configure(highlightbackground="#d9d9d9")
        self.Label5.configure(highlightcolor="black")
        self.Label5.configure(text='''Server IP:''')

        self.btnComSend = Button(self.frmCom)
        self.btnComSend.place(relx=0.21, rely=0.18, height=62, width=103)
        self.btnComSend.configure(activebackground="#d9d9d9")
        self.btnComSend.configure(activeforeground="#000000")
        self.btnComSend.configure(background="#d9d9d9")
        self.btnComSend.configure(command=ClientGUI_support.onSendtest)
        self.btnComSend.configure(foreground="#000000")
        self.btnComSend.configure(highlightbackground="#d9d9d9")
        self.btnComSend.configure(highlightcolor="black")
        self.btnComSend.configure(relief=RAISED)
        self.btnComSend.configure(text='''Send test''')

        self.Label6 = Label(self.frmCom)
        self.Label6.place(relx=0.64, rely=0.09, height=24, width=73)
        self.Label6.configure(activebackground="#f9f9f9")
        self.Label6.configure(activeforeground="black")
        self.Label6.configure(background="#d9d9d9")
        self.Label6.configure(foreground="#000000")
        self.Label6.configure(highlightbackground="#d9d9d9")
        self.Label6.configure(highlightcolor="black")
        self.Label6.configure(text='''Motor test''')

        self.btnMotor1L = Button(self.frmCom)
        self.btnMotor1L.place(relx=0.78, rely=0.09, height=38, width=87)
        self.btnMotor1L.configure(activebackground="#d9d9d9")
        self.btnMotor1L.configure(activeforeground="#000000")
        self.btnMotor1L.configure(background="#d9d9d9")
        self.btnMotor1L.configure(command=ClientGUI_support.on1L)
        self.btnMotor1L.configure(foreground="#000000")
        self.btnMotor1L.configure(highlightbackground="#d9d9d9")
        self.btnMotor1L.configure(highlightcolor="black")
        self.btnMotor1L.configure(relief=RAISED)
        self.btnMotor1L.configure(text='''(1) Left''')

        self.btnMotor1R = Button(self.frmCom)
        self.btnMotor1R.place(relx=0.78, rely=0.53, height=38, width=87)
        self.btnMotor1R.configure(activebackground="#d9d9d9")
        self.btnMotor1R.configure(activeforeground="#000000")
        self.btnMotor1R.configure(background="#d9d9d9")
        self.btnMotor1R.configure(command=ClientGUI_support.on1R)
        self.btnMotor1R.configure(foreground="#000000")
        self.btnMotor1R.configure(highlightbackground="#d9d9d9")
        self.btnMotor1R.configure(highlightcolor="black")
        self.btnMotor1R.configure(relief=RAISED)
        self.btnMotor1R.configure(text='''(1) Right''')

        self.btnMotor2R = Button(self.frmCom)
        self.btnMotor2R.place(relx=0.88, rely=0.53, height=38, width=87)
        self.btnMotor2R.configure(activebackground="#d9d9d9")
        self.btnMotor2R.configure(activeforeground="#000000")
        self.btnMotor2R.configure(background="#d9d9d9")
        self.btnMotor2R.configure(command=ClientGUI_support.on2R)
        self.btnMotor2R.configure(foreground="#000000")
        self.btnMotor2R.configure(highlightbackground="#d9d9d9")
        self.btnMotor2R.configure(highlightcolor="black")
        self.btnMotor2R.configure(relief=RAISED)
        self.btnMotor2R.configure(text='''(2) Right''')

        self.btnMotor2L = Button(self.frmCom)
        self.btnMotor2L.place(relx=0.88, rely=0.09, height=38, width=87)
        self.btnMotor2L.configure(activebackground="#d9d9d9")
        self.btnMotor2L.configure(activeforeground="#000000")
        self.btnMotor2L.configure(background="#d9d9d9")
        self.btnMotor2L.configure(command=ClientGUI_support.on2L)
        self.btnMotor2L.configure(foreground="#000000")
        self.btnMotor2L.configure(highlightbackground="#d9d9d9")
        self.btnMotor2L.configure(highlightcolor="black")
        self.btnMotor2L.configure(relief=RAISED)
        self.btnMotor2L.configure(text='''(2) Left''')

        self.Label7 = Label(self.frmCom)
        self.Label7.place(relx=0.65, rely=0.35, height=24, width=96)
        self.Label7.configure(activebackground="#f9f9f9")
        self.Label7.configure(activeforeground="black")
        self.Label7.configure(background="#d9d9d9")
        self.Label7.configure(foreground="#000000")
        self.Label7.configure(highlightbackground="#d9d9d9")
        self.Label7.configure(highlightcolor="black")
        self.Label7.configure(text='''Steps number''')

        self.txtStepNum = Entry(self.frmCom)
        self.txtStepNum.place(relx=0.67, rely=0.62,height=27, relwidth=0.09)
        self.txtStepNum.configure(background="white")
        self.txtStepNum.configure(font="TkFixedFont")
        self.txtStepNum.configure(foreground="#000000")
        self.txtStepNum.configure(highlightbackground="#d9d9d9")
        self.txtStepNum.configure(highlightcolor="black")
        self.txtStepNum.configure(insertbackground="black")
        self.txtStepNum.configure(selectbackground="#c4c4c4")
        self.txtStepNum.configure(selectforeground="black")

        self.txtVelocity = Entry(self.frmCom)
        self.txtVelocity.place(relx=0.45, rely=0.35, height=27, relwidth=0.09)
        self.txtVelocity.configure(background="white")
        self.txtVelocity.configure(font="TkFixedFont")
        self.txtVelocity.configure(foreground="#000000")
        self.txtVelocity.configure(highlightbackground="#d9d9d9")
        self.txtVelocity.configure(highlightcolor="black")
        self.txtVelocity.configure(insertbackground="black")
        self.txtVelocity.configure(selectbackground="#c4c4c4")
        self.txtVelocity.configure(selectforeground="black")

        self.btnTankConf = Button(self.frmCom)
        self.btnTankConf.place(relx=0.34, rely=0.18, height=62, width=103)
        self.btnTankConf.configure(activebackground="#d9d9d9")
        self.btnTankConf.configure(activeforeground="#000000")
        self.btnTankConf.configure(background="#d9d9d9")
        self.btnTankConf.configure(command=ClientGUI_support.onTankConfig)
        self.btnTankConf.configure(foreground="#000000")
        self.btnTankConf.configure(highlightbackground="#d9d9d9")
        self.btnTankConf.configure(highlightcolor="black")
        self.btnTankConf.configure(text='''Tank conf.''')
        self.btnTankConf.configure(width=103)

        self.frmLog = Frame(top)
        self.frmLog.place(relx=0.02, rely=0.64, relheight=0.29, relwidth=0.97)
        self.frmLog.configure(relief=GROOVE)
        self.frmLog.configure(borderwidth="2")
        self.frmLog.configure(relief=GROOVE)
        self.frmLog.configure(background="#d9d9d9")
        self.frmLog.configure(highlightbackground="#d9d9d9")
        self.frmLog.configure(highlightcolor="black")
        self.frmLog.configure(width=861)

        self.Label8 = Label(self.frmLog)
        self.Label8.place(relx=0.01, rely=0.03, height=24, width=30)
        self.Label8.configure(activebackground="#f9f9f9")
        self.Label8.configure(activeforeground="black")
        self.Label8.configure(background="#d9d9d9")
        self.Label8.configure(foreground="#000000")
        self.Label8.configure(highlightbackground="#d9d9d9")
        self.Label8.configure(highlightcolor="black")
        self.Label8.configure(text='''Log''')

        self.txtMainLog = Text(self.frmLog)
        self.txtMainLog.place(relx=0.01, rely=0.14, relheight=0.75
                , relwidth=0.98)
        self.txtMainLog.configure(background="white")
        self.txtMainLog.configure(font="TkTextFont")
        self.txtMainLog.configure(foreground="black")
        self.txtMainLog.configure(highlightbackground="#d9d9d9")
        self.txtMainLog.configure(highlightcolor="black")
        self.txtMainLog.configure(insertbackground="black")
        self.txtMainLog.configure(selectbackground="#c4c4c4")
        self.txtMainLog.configure(selectforeground="black")
        self.txtMainLog.configure(undo="1")
        self.txtMainLog.configure(width=842)
        self.txtMainLog.configure(wrap=WORD)

        self.frmLogClear = Button(self.frmLog)
        self.frmLogClear.place(relx=0.01, rely=0.89, height=22, width=70)
        self.frmLogClear.configure(activebackground="#d9d9d9")
        self.frmLogClear.configure(activeforeground="#000000")
        self.frmLogClear.configure(background="#d9d9d9")
        self.frmLogClear.configure(command=ClientGUI_support.onLogClear)
        self.frmLogClear.configure(foreground="#000000")
        self.frmLogClear.configure(highlightbackground="#d9d9d9")
        self.frmLogClear.configure(highlightcolor="black")
        self.frmLogClear.configure(text='''Clear''')

        self.Label14 = Label(self.frmLog)
        self.Label14.place(relx=0.13, rely=0.03, height=24, width=87)
        self.Label14.configure(activebackground="#f9f9f9")
        self.Label14.configure(activeforeground="black")
        self.Label14.configure(background="#d9d9d9")
        self.Label14.configure(foreground="#000000")
        self.Label14.configure(highlightbackground="#d9d9d9")
        self.Label14.configure(highlightcolor="black")
        self.Label14.configure(text='''Time runing:''')

        self.Label15 = Label(self.frmLog)
        self.Label15.place(relx=0.24, rely=0.03, height=24, width=180)
        self.Label15.configure(activebackground="#f9f9f9")
        self.Label15.configure(activeforeground="black")
        self.Label15.configure(background="#d9d9d9")
        self.Label15.configure(font=font12)
        self.Label15.configure(foreground="#0000fe")
        self.Label15.configure(highlightbackground="#d9d9d9")
        self.Label15.configure(highlightcolor="black")
        self.Label15.configure(text='''00:00''')


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

        self.txtStepNum.insert('0', 320)


        #print Args

        self.txtLogFolder.insert('0.0', self.LogFolderName)
        self.txtServerIP.insert('0', ServerIP)
        self.txtArgs.insert('0.0', Args)
        self.txtStatDaysBack.insert('0.0', self.Stat_days)
        self.txtStatArgs.insert('0.0', self.Stat_arg)
        temp_run_arg = "{} {} {} {}".format('fish_stat.py', self.LogFolderName, self.Stat_days, self.Stat_arg)
        self.txtStatRunArgs.insert('0.0', temp_run_arg)


    def print_and_update_main_log(self, str_to_print, new_line=True):
        global w, top
        str_temp = '{}'.format(str_to_print)
        print (str_temp)
        if new_line: str_temp = '{}\n'.format(str_temp)
        self.txtMainLog.insert(END, str_temp)
        self.txtMainLog.see(END)

    def update_time(self, time_str):
        self.Label15.configure(text=time_str)

    def __call__(self):
        print "RUN Command"




def make_two_digit_num(int_to_check):
    str_temp='{}'.format(int_to_check)
    if int_to_check<10: str_temp='0{}'.format(int_to_check)
    return str_temp

if __name__ == '__main__':
    vp_start_gui()

