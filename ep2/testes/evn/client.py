#!/usr/bin/python
'''
udp socket client
Silver Moon
'''
         
import socket   #for sockets
import select  
from time import sleep  
import sys  #for exit
         
# create dgram udp socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()
 
host = 'localhost';
port = 43278;

reply = 'nada'
while(reply != 'EXIT\n') :
    msg = raw_input('Enter message to send : ')
         
    try :
        #Set the whole string
        s.sendto(msg, (host, port))
        sleep(1)    
        # receive data from client (data, addr)
        while select.select([s,],[],[],0.0)[0]:                       
            d = s.recvfrom(1024)
            reply = d[0]
            addr = d[1]
                     
            print 'Server reply : ' + reply
                         
    except socket.error, msg:
        print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
