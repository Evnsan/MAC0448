#!/usr/bin/env python


'''
    Simple socket server using threads
'''
 
import socket
import sys
from thread import *
from sys import stdin
from udpmanager import udpmanager
from tcpmanager import tcpmanager


udpserver = udpmanager(3) #o argumento dos managers nao serve pra nd
tcpserver = tcpmanager(4)

#startando os threads dos servidores
udpserver.start()
tcpserver.start()

while 1:
    #wait to accept a connection - blocking call
    userinput = raw_input();
    print userinput


