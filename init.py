#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import *

class AppDriver(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.geometry("320x240+0+0")
        container = Frame(self, background="#ff0000")
        container.pack(fill=BOTH)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Welcome, Dash):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            frame.grid(row=0, column=0, sticky="news")
            self.frames[page_name] = frame

        self.show_frame("Welcome")

    def show_frame(self, page_name):
        print "showing "+page_name
        frame = self.frames[page_name]
        frame.tkraise()


class Dash(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, background="#0f0")            
        self.parent = parent
        self.controller = controller
        self.initUI()

    def initUI(self):
        self.pack()

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
    app.mainloop()

if __name__ == '__main__':
    main()