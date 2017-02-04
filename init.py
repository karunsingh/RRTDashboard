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

        self.container.rpmpercent = 0.0

        self.frames = {}
        for F in (Welcome, Dash):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            frame.grid(row=0, column=0, sticky="news")
            self.frames[page_name] = frame

        self.show_frame("Welcome")

        self.update_charge(100)
        self.update_speed(0)
        self.update_rpm(0)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if (page_name == "Dash"):
            net_thread = Thread(target=self.network_thread)
            net_thread.start()
            # warn_thread = Thread(target=frame.warning_thread)
            # warn_thread.start()

    def network_thread(self):
        s = socket.socket()
        # Uncomment exactly one of these!
        # computer-computer
        # host = socket.gethostname()
        # computer-pi (check host printed by tcpserver!)
        host = '169.254.0.1'
        # pi-pi
        # host = '169.254.233.59'
        port = 12345
        s.connect((host, port))
        while 1:
            data = s.recv(512)
            print "RECEIVED: "+ data
            j = json.loads(data)
            if j['type'] == 'charge':
                self.update_charge(j['payload'])
            elif j['type'] == 'speed':
                self.update_speed(j['payload'])
            elif j['type'] == 'heat':
                self.update_heat(j['payload'])
            elif j['type'] == 'fault':
                self.update_fault(j['payload'])
            elif j['type'] == 'rpm':
                self.update_rpm(j['payload'])

    def update_charge(self, data):
        self.container.chargelevel = int(data)
        self.container.charge.set(str(self.container.chargelevel)+"%")
        self.frames['Dash'].update_ui()
        print "Updated UI after charge"

    def update_speed(self, data):
        self.container.speedlevel = int(data)
        self.container.speed.set(str(self.container.speedlevel)+" kmph")
        self.frames['Dash'].update_ui() # doesn't do anything right now
        print "Updated UI after speed"

    def update_heat(self, data):
        if (data == True or data == 'true' or data == 'True'):
            self.container.is_heat = True
        else:
            self.container.is_heat = False
        self.frames['Dash'].update_ui()
        print "Updated UI after heat"

    def update_fault(self, data):
        if (data == True or data == 'true' or data == 'True'):
            self.container.is_fault = True
        else:
            self.container.is_fault = False
        self.frames['Dash'].update_ui()
        print "Updated UI after fault"

    def update_rpm(self, data):
        max_rpm = 4000.0
        percent = int(data)/max_rpm
        self.container.rpmpercent = percent
        self.frames['Dash'].update_ui()
        print "Updated UI after RPM"



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
        self.spd = Label(self, textvariable=self.parent.speed, font=("System", 24), fg="#fff", bg="#000")
        self.spd.grid(row=1, rowspan=8, column=1, columnspan=3, sticky="ns")
        self.heat = Label(self, text="Overheat", font=("System", 16), fg="#777", bg="#eee", relief=GROOVE, bd=2)
        self.heat.grid(row=9, rowspan=1, column=0, columnspan=2, sticky="news")
        self.fault = Label(self, text="Critical fault", font=("System", 16), fg="#777", bg="#eee", relief=GROOVE, bd=2)
        self.fault.grid(row=9, rowspan=1, column=2, columnspan=2, sticky="news")

        # RPM indicator
        self.rpm1 = Label(self, bg="#9ed8ed", relief=GROOVE)
        self.rpm1.grid(row=1, rowspan=1, column=0, columnspan=1, sticky="news")
        self.rpm2 = Label(self, bg="#9ed8ed", relief=GROOVE)
        self.rpm2.grid(row=2, rowspan=1, column=0, columnspan=1, sticky="news")
        self.rpm3 = Label(self, bg="#f4abab", relief=GROOVE)
        self.rpm3.grid(row=3, rowspan=1, column=0, columnspan=1, sticky="news")
        self.rpm4 = Label(self, bg="#f4abab", relief=GROOVE)
        self.rpm4.grid(row=4, rowspan=1, column=0, columnspan=1, sticky="news")
        self.rpm5 = Label(self, bg="#f4abab", relief=GROOVE)
        self.rpm5.grid(row=5, rowspan=1, column=0, columnspan=1, sticky="news")
        self.rpm6 = Label(self, bg="#abeaa4", relief=GROOVE)
        self.rpm6.grid(row=6, rowspan=1, column=0, columnspan=1, sticky="news")
        self.rpm7 = Label(self, bg="#abeaa4", relief=GROOVE)
        self.rpm7.grid(row=7, rowspan=1, column=0, columnspan=1, sticky="news")
        self.rpm8 = Label(self, bg="#abeaa4", relief=GROOVE)
        self.rpm8.grid(row=8, rowspan=1, column=0, columnspan=1, sticky="news")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=0)
        self.grid_rowconfigure(5, weight=0)
        self.grid_rowconfigure(6, weight=0)
        self.grid_rowconfigure(7, weight=0)
        self.grid_rowconfigure(8, weight=0)
        self.grid_rowconfigure(9, weight=1)
        self.grid()

    def update_ui(self):
        if self.parent.chargelevel >= 75:
            self.btry.config(bg="#26d300")
        elif self.parent.chargelevel >= 50:
            self.btry.config(bg="#bfff00")
        elif self.parent.chargelevel >= 25:
            self.btry.config(bg="#fc8711")
        else:
            self.btry.config(bg="#f00")

        if self.parent.is_heat == True:
            self.heat.config(bg="#f00", fg="#fff")
        else:
            self.heat.config(bg="#eee", fg="#777")

        if self.parent.is_fault == True:
            self.fault.config(bg="#f00", fg="#fff")
        else:
            self.fault.config(bg="#eee", fg="#777")

        if self.parent.rpmpercent > 0:
            self.rpm8.config(bg="#5fc43a")
        else:
            self.rpm8.config(bg="#abeaa4")
        if self.parent.rpmpercent > 1/8.0:
            self.rpm7.config(bg="#5fc43a")
        else:
            self.rpm7.config(bg="#abeaa4")
        if self.parent.rpmpercent > 2/8.0:
            self.rpm6.config(bg="#5fc43a")
        else:
            self.rpm6.config(bg="#abeaa4")

        if self.parent.rpmpercent > 3/8.0:
            self.rpm5.config(bg="#b52626")
        else:
            self.rpm5.config(bg="#f4abab")
        if self.parent.rpmpercent > 4/8.0:
            self.rpm4.config(bg="#b52626")
        else:
            self.rpm4.config(bg="#f4abab")
        if self.parent.rpmpercent > 5/8.0:
            self.rpm3.config(bg="#b52626")
        else:
            self.rpm3.config(bg="#f4abab")

        if self.parent.rpmpercent > 6/8.0:
            self.rpm2.config(bg="#4272b2")
        else:
            self.rpm2.config(bg="#9ed8ed")
        if self.parent.rpmpercent > 7/8.0:
            self.rpm1.config(bg="#4272b2")
        else:
            self.rpm1.config(bg="#9ed8ed")

    """def warning_thread(self):
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
            self.fault_state = 0"""


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
    # Remove title bar:
    app.overrideredirect(1)
    app.mainloop()

if __name__ == '__main__':
    main()