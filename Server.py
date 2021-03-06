#!/usr/bin/env python
import socket
import pickle

TCP_IP = '127.0.0.3'
TCP_PORT = 5005
BUFFER_SIZE = 100000  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print('Starting Hand Interprator Server')
print('Connection address:', addr)

while 1:
    data = conn.recv(BUFFER_SIZE)
    #if not data: break
    if data: 
        # call the interpretator
        capture = pickle.loads(data)
        print ('I have recieved something')
        print ('received data:', capture)
    conn.send(data)  # echo
