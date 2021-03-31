# -*- coding: utf-8 -*-
# TCP Server ECHO Code
import socket
import signal
import sys
 
"""
NOTE: Signal library behave differently on Windows/Mac, 
Ctrl+C does not work on Windows (Unable to break the socket)
"""

def signal_handler(signal, frame):
    print ('You pressed Ctrl+C!')
    s.close()
    sys.exit(0)
 
signal.signal(signal.SIGINT, signal_handler)
 
print ('Server Running at ', socket.gethostbyname(socket.gethostname()) )
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('',7)) #Any address, Any port
s.listen(1)
 
while True:
    conn, addr = s.accept()
    print ('Connected by', addr)
    while True:
        data = conn.recv(1024)
        print(data)
        if not data: break
        conn.sendall(data)
    conn.close()