#!/usr/bin/python           # This is server.py file

import socket               # Import socket module
import json

s = socket.socket()         # Create a socket object
host = '169.254.0.1' # Get local machine name
port = 12345                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

print host
s.listen(5)                 # Now wait for client connection.
while True:
   c, addr = s.accept()     # Establish connection with client.
   print 'Got connection from', addr
   while True:
      inp = raw_input("Enter data: ")
      if inp[0] == 'f':
      	data = json.dumps({'type':'fault', 'payload':inp[1:]})
      elif inp[0] == 's':
      	data = json.dumps({'type':'speed', 'payload':inp[1:]})
      elif inp[0] == 'c':
      	data = json.dumps({'type':'charge', 'payload':inp[1:]})
      elif inp[0] == 'h':
      	data = json.dumps({'type':'heat', 'payload':inp[1:]})
      elif inp[0] == 'r':
      	data = json.dumps({'type':'rpm', 'payload':inp[1:]})
      c.send(data)
   c.close()                # Close the connection