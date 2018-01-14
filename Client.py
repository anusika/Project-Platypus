 #!/usr/bin/env python

import socket  
import multiprocessing as mp
import time
import sys
import tty
import termios
import pickle

sys.path.append("./LeapAnalyzer")
import LeapOutput 

TCP_IP = '127.0.0.3'
TCP_PORT = 5005
BUFFER_SIZE = 100000
MESSAGE = "Hello, World!"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

print "Welcome to Project Platypus"
print "---------------------------"
print "Press any key to start recording"

def get_ch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def worker():
    while True:
        time.sleep(2)

def countDownFrom3():
    print "It will record in 3"
    time.sleep(1)
    print "It will record in 2"
    time.sleep(1)
    print "It will record in 1"
    time.sleep(1)
    print "Recording...",

p = mp.Process(target=worker)
p.start()
get_ch()
# once you finish recording 
countDownFrom3()
# get data and send it 
recording = LeapOutput.main()
print "Done recording, now need to pickle"
print recording[0]

## pretent 
# test = [[1,2,3,4,5,6,7,8,9,10], [11,12,13,14,15]]
dumped = pickle.dumps(recording)
print("Dumped size:")
print(sys.getsizeof(dumped))
s.send(dumped)
## when you recieve something 
data = s.recv(BUFFER_SIZE)

print "received data:", data

# terminate worker thread
p.terminate()