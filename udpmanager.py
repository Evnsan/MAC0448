#!/usr/bin/env python

import socket
import sys
from sys import stdin
from threading import Thread
from _dbus_bindings import Boolean

#SERVER UDP CONFIG

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port

try :
    sudp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'Socket created'
except socket.error, msg :
    print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
    
    
    
try:
    sudp.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete UDP'



class udpmanager (Thread):

    def __init__(self, val):
        Thread.__init__(self)
        self.val = val
        
        
    def run(self):
        print 'toaqui3'
        while 1:
            d = sudp.recvfrom(1024)
            data = d[0]
            addr = d[1]
         
            if not data: 
                break
         
            reply = 'OK...' + data
            print 'toaqui4'
    
            sudp.sendto(reply , addr)
            print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data.strip()
        sudp.close()
        print 'desligando servidor udp'
     


