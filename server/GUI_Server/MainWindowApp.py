# $Id: MainWindowApp.py,v 1.3 2004/04/12 04:46:16 prof Exp $
import Tkinter
import logging
import CumulativeLogger
import gettext
import os
import socket
import threading
import sys


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

class MainWindowApp(Tkinter.Tk):

    def __init__(self, log):

        self.log = log
        self.logger = logging.getLogger(self.__class__.__name__)
        #cumL = CumulativeLogger.__name__
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

    def onConnect(self):
        # Echo client program

        HOST = '192.168.1.7'  # The remote host
        PORT = 50007  # The same port as used by the server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((HOST, PORT))
            s.send(self.i)
            data = s.recv(1024)
            s.close()
            self.logger.info(_('Received %s'), repr(data))
        except socket.error, v:
            errorcode = v[0]
            self.logger.info(_("%s (%i)"), os.strerror(errorcode), errorcode)



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
        if not str_to_add=="":
            if str_to_add=="/del":
                self.txt_del_last_char()
            else:
                if new_line==True:
                    self.txt.insert(Tkinter.END, '{}{}'.format(str_to_add, "\n"))
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
    global exit_var
    request = client_socket.recv(1024)
    str_tmp = 'Received {}'.format(request)
    app.onTxtUpdate(str_tmp)
    l.info(str_tmp)
    if request=='Close': exit_var=True
    client_socket.send(request)
    client_socket.close()


def while_true_func(server):
    global exit_var
    global connected
    global first_accp_conn
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
            str_tmp = 'Accepted connection from {}:{}'.format(address[0], address[1])
            app.onTxtUpdate(' ')
            if first_accp_conn:
                app.onTxtUpdate(str_tmp)
                first_accp_conn=False

            l.info(str_tmp)
            client_handler = threading.Thread(
                target=handle_client_connection,
                args=(client_sock,)
                # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
            )
            client_handler.start()
            line_counter=0
            line_dir=1
        except:
            pass
    connected=False
    return True


app = MainWindowApp(cl, )
app.run()
