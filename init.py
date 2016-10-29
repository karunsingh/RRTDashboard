#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import *
import ttk
from time import sleep
from threading import Thread
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

        self.container.chargelevel = 100

        self.container.charge = StringVar()
        self.container.charge.set(str(self.container.chargelevel)+"%")

        self.frames = {}
        for F in (Welcome, Dash):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            frame.grid(row=0, column=0, sticky="news")
            self.frames[page_name] = frame

        self.show_frame("Welcome")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        # Begin simulation
        if (page_name == "Dash"):
            thread = Thread(target=self.network_thread)
            thread.start()

    def network_thread(self):
        s = socket.socket()
        # Uncomment exactly one of these!
        #host = socket.gethostname() - computer-computer
        #host = '169.254.0.1' - computer-pi
        #host = '169.254.233.59' - pi-pi
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

    def update_charge(self, data):
        self.container.chargelevel = int(data)
        self.container.charge.set(str(self.container.chargelevel)+"%")
        self.frames['Dash'].update_ui()

    def update_speed(self, data):
        self.container.speed.set(data+" kmph")
        self.frames['Dash'].update_ui() # doesn't do anything right now


class Dash(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, background="#000")            
        self.parent = parent
        self.controller = controller
        self.initUI()

    def initUI(self):
        #b = Button(self, text="Back", command=lambda: self.controller.show_frame("Welcome"), bd=0,
            #bg="#f00", fg="#fff", padx=10, pady=5)
        #b.grid(row=0, rowspan=1, column=3, columnspan=1, sticky="ne")
        self.btry = Label(self, textvariable=self.parent.charge, font=("System", 20), fg="#000", bg="#fff")
        self.btry.grid(row=0, rowspan=1, column=0, columnspan=4, sticky="news")
        spd = Label(self, textvariable=self.parent.speed, font=("System", 30), fg="#fff", bg="#000")
        spd.grid(row=1, rowspan=1, column=0, columnspan=4, sticky="ns")
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
            self.btry.config(bg="#34ed3d")
        elif self.parent.chargelevel >= 50:
            self.btry.config(bg="#eded34")
        elif self.parent.chargelevel >= 25:
            self.btry.config(bg="#fc8711")
        else:
            self.btry.config(bg="#f00")
        

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