import socket
import sys
from sys import stdin
from threading import Thread
from thread import *


HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print 'Socket created'
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete TCP'
 
#Start listening on socket
s.listen(10)


print 'Socket now listening'

def clientthread(conn):
#Sending message to connected client
    conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
     
    #infinite loop so that function do not terminate and thread do not end.
    while True:
         
        #Receiving from client
        data = conn.recv(1024)
        reply = 'OK...' + data
        if not data: 
            break
        conn.sendall(reply)
     
    #came out of loop
    conn.close()


class tcpmanager (Thread):
             
    def __init__(self, val):
        Thread.__init__(self)
        self.val = val
        
        
    def run(self):
        print s
        while ONLINE:
            conn, addr = s.accept()
            
            print 'Connected with ' + addr[0] + ':' + str(addr[1])
        
        #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
            start_new_thread(clientthread ,(conn,))
        s.close()
     
     
