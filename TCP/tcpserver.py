#!/usr/bin/python           # This is server.py file

import socket               # Import socket module
import json

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.
while True:
   c, addr = s.accept()     # Establish connection with client.
   print 'Got connection from', addr
   while True:
      speed = raw_input("New battery: ")
      data = json.dumps({'type':'heat', 'payload':speed})
      c.send(data)
   c.close()                # Close the connection