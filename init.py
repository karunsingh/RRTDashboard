#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import *
import ttk
from time import sleep
from threading import Thread
import threading
import socket
import json

class AppDriver(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.geometry("320x240+0+0")
        self.container = Frame(self, background="#ff0000")
        self.container.pack(fill=BOTH)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.container.speed = StringVar()
        self.container.speed.set("0 kmph")

        self.container.charge = StringVar()

        self.container.is_heat = False
        self.container.is_fault = False

        self.frames = {}
        for F in (Welcome, Dash):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            frame.grid(row=0, column=0, sticky="news")
            self.frames[page_name] = frame

        self.show_frame("Welcome")

        self.update_charge(100)
        self.update_speed(0)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if (page_name == "Dash"):
            net_thread = Thread(target=self.network_thread)
            net_thread.start()
            warn_thread = Thread(target=frame.warning_thread)
            warn_thread.start()

    def network_thread(self):
        s = socket.socket()
        # Uncomment exactly one of these!
        # computer-computer
        host = socket.gethostname()
        # computer-pi
        # host = '169.254.0.1'
        # pi-pi
        # host = '169.254.233.59'
        port = 12345
        s.connect((host, port))
        while 1:
            data = s.recv(512)
            print "RECEIVED: ", data
            j = json.loads(data)
            if j['type'] == 'charge':
                self.update_charge(j['payload'])
            elif j['type'] == 'speed':
                self.update_speed(j['payload'])
            elif j['type'] == 'heat':
                self.update_heat(j['payload'])
            elif j['type'] == 'fault':
                self.update_fault(j['payload'])

    def update_charge(self, data):
        self.container.chargelevel = int(data)
        self.container.charge.set(str(self.container.chargelevel)+"%")
        self.frames['Dash'].update_ui()

    def update_speed(self, data):
        self.container.speedlevel = int(data)
        self.container.speed.set(str(self.container.speedlevel)+" kmph")
        self.frames['Dash'].update_ui() # doesn't do anything right now

    def update_heat(self, data):
        if (data == True or data == 'true' or data == 'True'):
            self.container.is_heat = True
        else:
            self.container.is_heat = False

    def update_fault(self, data):
        if (data == True or data == 'true' or data == 'True'):
            self.container.is_fault = True
        else:
            self.container.is_fault = False


class Dash(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, background="#000")            
        self.parent = parent
        self.controller = controller
        self.initUI()
        self.heat_state = 0
        self.fault_state = 0

    def initUI(self):
        self.btry = Label(self, textvariable=self.parent.charge, font=("System", 20), fg="#000", bg="#fff")
        self.btry.grid(row=0, rowspan=1, column=0, columnspan=4, sticky="news")
        self.spd = Label(self, textvariable=self.parent.speed, font=("System", 30), fg="#fff", bg="#000")
        self.spd.grid(row=1, rowspan=1, column=0, columnspan=4, sticky="ns")
        self.heat = Label(self, text="Overheat", font=("System", 16), fg="#777", bg="#eee", relief=GROOVE, bd=2)
        self.heat.grid(row=2, rowspan=1, column=0, columnspan=2, sticky="news")
        self.fault = Label(self, text="Critical fault", font=("System", 16), fg="#777", bg="#eee", relief=GROOVE, bd=2)
        self.fault.grid(row=2, rowspan=1, column=2, columnspan=2, sticky="news")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=4)
        self.grid_rowconfigure(2, weight=1)
        self.grid()

    def update_ui(self):
        if self.parent.chargelevel >= 75:
            self.btry.config(bg="#26d300")
        elif self.parent.chargelevel >= 50:
            self.btry.config(bg="#eded34")
        elif self.parent.chargelevel >= 25:
            self.btry.config(bg="#fc8711")
        else:
            self.btry.config(bg="#f00")

    def warning_thread(self):
        threading.Timer(0.5, self.warning_thread).start()

        if (self.heat_state == 0 and self.parent.is_heat == True):
            self.heat.config(bg="#f00", fg="#fff")
            self.heat_state = 1
        else:
            self.heat.config(bg="#eee", fg="#777")
            self.heat_state = 0

        if (self.fault_state == 0 and self.parent.is_fault == True):
            self.fault.config(bg="#f00", fg="#fff")
            self.fault_state = 1
        else:
            self.fault.config(bg="#eee", fg="#777")
            self.fault_state = 0


class Welcome(Frame):
  
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, background="#ededed")            
        self.parent = parent
        self.controller = controller
        self.initUI()

    def initUI(self):
        photo = PhotoImage(file="RRTLogo.gif")
        label = Label(self, image=photo, height=200)
        label.image = photo
        
        b = Button(self, text="Enter Dashboard", 
            command=lambda: self.controller.show_frame("Dash"), bd=0, 
            bg="#000", fg="#fff", height=40)
        label.pack(side=TOP, fill=X)
        b.pack(side=BOTTOM, fill=X)
        
        self.pack()

def main():
    app = AppDriver()
    # Title bar:
    # app.overrideredirect(1)
    app.mainloop()

if __name__ == '__main__':
    main()