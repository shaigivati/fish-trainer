# $Id: MainWindowApp.py,v 1.3 2004/04/12 04:46:16 prof Exp $
import Tkinter
import logging
import CumulativeLogger
import gettext
import os
import socket
import threading
import sys
import ConfigParser
import ast
import feeder

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

_ = gettext.gettext
exit_var = False
connected = False
kill_all = False
first_accp_conn = True

logging.basicConfig()
l = logging.getLogger()
l.setLevel(logging.INFO)
cl = CumulativeLogger.CumulativeLogger()
l.info(_('Program started.'))
Config = ConfigParser.ConfigParser()
feed = feeder.Feeder


class MainWindowApp(Tkinter.Tk):

    def __init__(self, log):
        global feed
        self.log = log
        self.logger = logging.getLogger(self.__class__.__name__)
        #cumL = CumulativeLogger.__name__

        Config.read('GUI_config.txt')
        self.step_num = ConfigSectionMap("Motor settings")['steps']
        self.Pin_en = {}
        self.Pin_en[1] = ConfigSectionMap("Motor settings")['enable pin 1']
        self.Pin_en[2] = ConfigSectionMap("Motor settings")['enable pin 2']

        self.Pin={}
        self.Pin['1L'] = ConfigSectionMap("Tank")['tank 1 left pin']
        self.Pin['1R'] = ConfigSectionMap("Tank")['tank 1 right pin']
        self.Pin['2L'] = ConfigSectionMap("Tank")['tank 2 left pin']
        self.Pin['2R'] = ConfigSectionMap("Tank")['tank 2 right pin']
        self.Pin['2LD'] = ConfigSectionMap("Tank")['tank 2 left direction pin']
        self.Pin['2RD'] = ConfigSectionMap("Tank")['tank 2 right direction pin']

        feed = feeder.Feeder({self.Pin_en[1], self.Pin['1L'], self.Pin['1R'], self.Pin_en[2], self.Pin['2L'], self.Pin['2R'], self.Pin['2LD'], self.Pin['2RD']})

        add_step = feed.add_program_step(1, 'left', 360*4, 100, 10)
        add_step = feed.add_program_step(2, 'wait', 4)
        add_step = feed.add_program_step(3, 'left', 360*4, 600, 20)

        #add_step = feed.add_program_step(9, 'wait', 3)
        #add_step = feed.add_program_step(10, 'left', (2*360-45), 400, 15)
        #add_step = feed.add_program_step(11, 'wait', 10, 0.2)
        #add_step = feed.add_program_step(12, 'right', 30, 100, 6)
        #add_step = feed.add_program_step(13, 'wait', 10, 0.4)
        #add_step = feed.add_program_step(14, 'left', 20, 100, 6)
        #add_step = feed.add_program_step(15, 'wait', 10, 0.4)
        #add_step = feed.add_program_step(16, 'right', 20, 100, 6)

        #add_step = feed.add_program_step(1, 'left', 3200, 200, 5)
        #add_step = feed.add_program_step(1, 'wait', 0.8)
        #add_step = feed.add_program_step(2, 'left', 45 + 90 + 60, 100, 5)
        #add_step = feed.add_program_step(3, 'wait', 0.5)
        #add_step = feed.add_program_step(4, 'right', 20, 60, 10)
        #add_step = feed.add_program_step(5, 'wait', 0.2)
        #add_step = feed.add_program_step(6, 'left', 20, 60, 10)
        #add_step = feed.add_program_step(7, 'wait', 0.6)
        #add_step = feed.add_program_step(8, 'right', 180+90, 150, 15)

        #self.Pin={'1L':1 , '1R':2 , '2L':3 , '2R':4}
        #print ('[1,left]:{}, [1,right]:{}, [2,left]:{}, [2,right]:{}'.format(self.Pin['1L'], self.Pin['1R'], self.Pin['2L'], self.Pin['2R']))
        self.i=0

    def run(self):
        """ Create and run GUI """
        self.root = root = Tkinter.Tk()
        root.title(_('Fish Training GUI - Server'));

        But_frame = Tkinter.Frame(root, width=100, height=100)

        Tkinter.Button(But_frame, text=_('Connect'), command=self.onConnectServer, width=10).pack(side=Tkinter.LEFT)
        #Tkinter.Button(But_frame, text=_('View Log'), command=self.onViewLog, width=10).pack(side=Tkinter.LEFT)
        Tkinter.Button(But_frame, text=_('Exit'), command=self.onExit, width=10).pack(side=(Tkinter.LEFT))

        But_frame.pack(side=Tkinter.BOTTOM)

        # create a Frame for the Text and Scrollbar
        txt_frm = Tkinter.Frame(self.root, width=600, height=600)
        txt_frm.pack(fill="both", expand=True)
        # ensure a consistent GUI size
        txt_frm.grid_propagate(False)
        # implement stretchability
        txt_frm.grid_rowconfigure(0, weight=1)
        txt_frm.grid_columnconfigure(0, weight=1)

        # create a Text widget
        self.txt = Tkinter.Text(txt_frm, borderwidth=3, relief="sunken")
        self.txt.config(font=("consolas", 12), undo=True, wrap='word')
        self.txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        # create a Scrollbar and associate it with txt
        scrollb = Tkinter.Scrollbar(txt_frm, command=self.txt.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        self.txt['yscrollcommand'] = scrollb.set

        root.wm_attributes("-topmost", 1)
        root.focus_force()

        temp_txt = self.log.getText()
        self.logger.info(temp_txt)
        self.onTxtUpdate(temp_txt)

        self.onConnectServer()

        root.mainloop()


    def onExit(self):
        global exit_var
        global kill_all
        global connected

        """ Process 'Exit' command """
        exit_var=True
        kill_all=True
        connected=False
        #self.ConnectLoop()

        self.root.quit()

        sys.exit(1)

    def onViewLog(self):
        #ViewLog.ViewLog(self.root, self.log)
        #self.txt.insert('10.0',self.txt.index('10.0'))

        #self.txt.delete('1.{}'.format(len(self.txt.get('1.0', '2.0'))-2), Tkinter.END)
        dot_index = self.txt.index(Tkinter.END).find('.')
        int_last_line = int(self.txt.index(Tkinter.END)[0:dot_index])
        temp_line_no = '{}.0'.format(int_last_line-1)
        last_line_len = len(self.txt.get(temp_line_no,Tkinter.END))

        if last_line_len == 1:
            int_last_line-=1
            temp_line_no = '{}.0'.format(int_last_line - 1)
            last_line_len = len(self.txt.get(temp_line_no, Tkinter.END))

        #print 'temp_line_no:{}'.format(temp_line_no)
        #print ('last line len:{}'.format(last_line_len))
        last_char_index = '{}.{}'.format(int_last_line-1, last_line_len-2)
        #print 'last_char_index:{}'.format(last_char_index)
        self.txt.delete(last_char_index, Tkinter.END)


    def onConnectServer(self):

        self.root.after(100, self.ConnectLoop())
        self.root.mainloop()

    def ConnectLoop(self):
        global exit_var
        global kill_all
        global connected
        global I
        # while not kill_all:
        #print("kill_all", kill_all, "connected", connected)
        self.onTxtUpdate("")
        #self.logger.info(I)
        #I+=1
        if not connected and not kill_all:
            exit_var = False
            #bind_ip = '0.0.0.0'
            bind_port = 50007
            try:
                bind_ip = get_ip()
                temp_txt = 'My IP-{}'.format(bind_ip)
                self.logger.info(temp_txt)
                self.onTxtUpdate(temp_txt)
                server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server.bind((bind_ip, bind_port))
                server.listen(5)  # max backlog of connections
                server.settimeout(0.1)
                try_while_true = threading.Thread(
                    target=while_true_func,
                    args=(server, )
                )
                try_while_true.start()
                connected = True
                temp_txt = 'Listening on {}:{}'.format(bind_ip, bind_port)
                self.logger.info(temp_txt)
                self.onTxtUpdate(temp_txt)
            except socket.error as e:
                self.logger.info('Socket exception: %s', str(e) or repr(e))

                #except socket.error, msg:
                #self.logger.info(_('[ERROR]'), msg[0], msg[1])
                #if msg[0] == 98: server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server.close()
        if not kill_all: self.root.after(10,self.ConnectLoop)

    def onTxtUpdate(self, str_to_add="", new_line=True):

        #self.txt.delete(0.0,100.0)
        #self.txt.insert(Tkinter.END, self.log.getText())
        if not str_to_add == "":
            if str_to_add == "/del":
                self.txt_del_last_char()
            else:
                if new_line == True:
                    self.txt.insert(Tkinter.END, '{}{}'.format("\n",str_to_add))
                else:
                    self.txt.insert(Tkinter.END, '{}'.format(str_to_add))
        self.txt.see(Tkinter.END)


    def txt_del_last_char(self):
        dot_index = self.txt.index(Tkinter.END).find('.')
        int_last_line = int(self.txt.index(Tkinter.END)[0:dot_index])
        temp_line_no = '{}.0'.format(int_last_line - 1)
        last_line_len = len(self.txt.get(temp_line_no, Tkinter.END))

        if last_line_len == 1:
            int_last_line -= 1
            temp_line_no = '{}.0'.format(int_last_line - 1)
            last_line_len = len(self.txt.get(temp_line_no, Tkinter.END))

        # print 'temp_line_no:{}'.format(temp_line_no)
        # print ('last line len:{}'.format(last_line_len))
        last_char_index = '{}.{}'.format(int_last_line - 1, last_line_len - 2)
        # print 'last_char_index:{}'.format(last_char_index)
        self.txt.delete(last_char_index, Tkinter.END)

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def handle_client_connection(client_socket):
    global exit_var, line_counter, line_dir
    request = client_socket.recv(1024)
    client_socket.send(request)            #echo
    str_tmp = 'Received {}'.format(request)
    app.onTxtUpdate('{}'.format(str_tmp), False)
    dict_data = ast.literal_eval(request)
    #app.onTxtUpdate('id:{}, side:{}'.format(dict_data['id'], dict_data['side']))
    recv_id = str(dict_data['id'])
    recv_side = dict_data['side']

    l.info(str_tmp)
    line_counter = -1
    line_dir = 1
    if request == 'Close': exit_var=True

    client_socket.close()
    print ("rec_id:{0}".format(recv_id))

    if recv_id == "1":
        pin_num_str = '{0}{1}'.format(recv_id, (recv_side[0:1]).upper()) #create 1L/1R str
        #print('-->{}'.format(app.Pin[pin_num_str]))
        spin_res = feed.spin(int(app.Pin[pin_num_str]), int(app.step_num), int(app.Pin_en[1]))
        app.onTxtUpdate('{0}.'.format(spin_res), False)
    if recv_id == "2":
        pin_num_str = '{0}{1}'.format(recv_id, (recv_side[0:1]).upper())
        pin_dir_str = '{0}{1}'.format(pin_num_str, 'D')  # create 1L/1R str
        print ("recv_id={0}, side:{1}".format(pin_num_str[0], pin_num_str[1]))
        spin_res = feed.spin_program(int(app.Pin[pin_num_str]), int(app.Pin[pin_dir_str]), int(app.Pin_en[2]))
        app.onTxtUpdate('{0}.'.format(spin_res), False)
    if recv_id == "test_1L":
        pin_num_str = '1L'
        step_no = int(recv_side)
        spin_res = feed.spin(int(app.Pin[pin_num_str]), step_no, int(app.Pin_en[1]))
        app.onTxtUpdate('{0}.'.format(spin_res), False)
    if recv_id == "test_1R":
        pin_num_str = '1R'
        step_no = int(recv_side)
        spin_res = feed.spin(int(app.Pin[pin_num_str]), step_no, int(app.Pin_en[1]))
        app.onTxtUpdate('{0}.'.format(spin_res), False)
    if recv_id == "test_2L":
        pin_num_str = '2L'
        step_no = int(recv_side)
        pin_dir_str = '{0}{1}'.format(pin_num_str, 'D')  # create 1L/1R str
        # print('-->{}'.format(app.Pin[pin_num_str]))
        spin_res = feed.spin_program(int(app.Pin[pin_num_str]), int(app.Pin[pin_dir_str]), int(app.Pin_en[2]), step_no)
        app.onTxtUpdate('{0}.'.format(spin_res), True)
    if recv_id == "test_2R":
        pin_num_str = '2R'
        step_no = int(recv_side)
        pin_dir_str = '{0}{1}'.format(pin_num_str, 'D')  # create 1L/1R str
        # print('-->{}'.format(app.Pin[pin_num_str]))
        spin_res = feed.spin_program(int(app.Pin[pin_num_str]), int(app.Pin[pin_dir_str]), int(app.Pin_en[2]), step_no)
        app.onTxtUpdate('{0}.'.format(spin_res), True)

def while_true_func(server):
    global exit_var, connected, first_accp_conn, line_counter, line_dir
    line_counter=0
    line_dir=1
    while not exit_var:
        if line_counter>=30:
            line_dir*=-1
            line_counter=0

        if line_dir>0:
            app.onTxtUpdate(".", False)
        else:
            app.onTxtUpdate('/del', False)

        line_counter+=1
        sys.stdout.flush()
        try:
            client_sock, address = server.accept()
            str_tmp = '\nAccepted connection from {0}:{1}'.format(address[0], address[1])

            if first_accp_conn:
                app.onTxtUpdate(str_tmp)
                first_accp_conn=False

            l.info(str_tmp)
            client_handler = threading.Thread(
                target=handle_client_connection,
                args=(client_sock,)
                # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
            )
            app.onTxtUpdate(' ')
            client_handler.start()
            line_counter=-1
            line_dir=1
        except:
            pass
    connected=False
    return True


app = MainWindowApp(cl, )
app.run()
