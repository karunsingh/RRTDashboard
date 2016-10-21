#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import *
import ttk
from time import sleep
from threading import Thread
import socket

class AppDriver(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.geometry("320x240+0+0")
        container = Frame(self, background="#ff0000")
        container.pack(fill=BOTH)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.speed = StringVar()
        container.speed = self.speed
        self.speed.set("0 kmph")

        self.frames = {}
        for F in (Welcome, Dash):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
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

    def speed_test(self):
        for i in range(100):
            sleep(0.07)
            self.speed.set(str(i)+" kmph")

    def network_thread(self):
        s = socket.socket()
        host = '169.254.0.1'
        port = 12345
        s.connect((host, port))
        while 1:
            data = s.recv(512)
            print "RECEIVED: ", data
            self.speed.set(data+" kmph")


class Dash(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, background="#000")            
        self.parent = parent
        self.controller = controller
        self.speed = self.parent.speed
        self.initUI()

    def initUI(self):
        """pb_hd = ttk.Progressbar(self, orient='horizontal', mode='determinate')
        pb_hd.pack(side=TOP)
        pb_hd.step(50)"""
        w = Label(self, textvariable=self.speed, font=("System", 30), fg="#fff", bg="#000")
        w.grid(row=1, rowspan=1, column=0, columnspan=4, sticky="n")
        b = Button(self, text="Back", command=lambda: self.controller.show_frame("Welcome"), bd=0,
            bg="#f00", fg="#fff", padx=10, pady=5)
        b.grid(row=0, rowspan=1, column=3, columnspan=1, sticky="ne")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)
        self.grid()
        

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
    app.overrideredirect(1)
    app.mainloop()

if __name__ == '__main__':
    main()