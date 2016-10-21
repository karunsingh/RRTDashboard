#!/usr/bin/python           # This is client.py file

import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = '169.254.0.1'        # Get local machine name
port = 12345                # Reserve a port for your service.

s.connect((host, port))
while 1:
    data = s.recv(512)
    print "RECEIVED: ", data