#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

arg_dict={'video': None, 'log': 'test', 'file': 'tank_config.txt'}

import Tkinter
from threading import Thread
from track_fish import main_tf
import multiprocessing

i=0

class simpleapp_tk(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()

        self.fish_no_txtbox = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self,textvariable=self.fish_no_txtbox)
        self.entry.grid(column=0,row=0,sticky='EW')
        self.entry.bind("<Return>", self.OnPressEnter)
        self.fish_no_txtbox.set(u"Enter fish no.")

        button_Run = Tkinter.Button(self,text=u"Run",
                                command=self.OnButtonClick_run)
        button_Run.grid(column=1,row=0)
        button_Stop = Tkinter.Button(self, text=u"Stop",
                                command=self.OnButtonClick_stop)
        button_Stop.grid(column=1, row=1)

        self.labelVariable = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelVariable,
                              anchor="w",fg="white",bg="blue")
        label.grid(column=0,row=2,columnspan=2,sticky='EW')
        self.labelVariable.set(u"")

        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)
        self.update()

        #self.geometry(self.geometry())
        FrameSizeX=287
        FrameSizeY=147
        FramePosX=20
        FramePosY=20
        self.geometry("%sx%s+%s+%s" % (FrameSizeX,FrameSizeY,FramePosX,FramePosY))
        print self.geometry()
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

    def OnButtonClick_run(self):
        global i
        i=0
        self.labelVariable.set( self.fish_no_txtbox.get()+" (Run)" )
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)
        fish_no=self.fish_no_txtbox.get()
        arg_dict = {'video': None, 'log': fish_no, 'file': 'tank_config.txt'}
        multiprocessing.Process(target=main_tf,
                                args=(arg_dict, in_queue)).start()

    def OnButtonClick_stop(self):
        global i
        i=5
        in_queue.put(i)
        self.labelVariable.set( self.fish_no_txtbox.get()+" (Stop)" )
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)


    def OnPressEnter(self,event):
        global i
        self.labelVariable.set( self.fish_no_txtbox.get()+" (You pressed ENTER)" )
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)
        i+=1
        in_queue.put(i)
        #thread.join()


if __name__ == "__main__":

    print "done"
    app = simpleapp_tk(None)
    app.title('track_fish GUI')
    in_queue = multiprocessing.Queue()
    #in_queue.put(1)
    #p = Process(target=main_tf(arg_dict,in_queue))

    app.mainloop()
