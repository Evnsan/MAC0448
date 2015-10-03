#!/usr/bin/env python

# Filename: HeartbeatClient.py

"""Heartbeat client, sends out an UDP packet periodically"""

import socket, time, threading, sys

SERVER_IP = '127.0.0.1'; SERVER_PORT = 43278; BEAT_PERIOD = 11 

class lstUDP(threading.Thread):
    def __init__(self, sock):
        self.sock = sock
        super(lstUDP, self).__init__()
    def run(self):
        try:
            # Receive response
            print >>sys.stderr, 'waiting to receive'
            data, server = self.sock.recvfrom(4096)
            print >>sys.stderr, 'received "%s"' % data

        finally:
            print >>sys.stderr, 'closing socket'
            self.sock.close()

class main():
    print ('Sending heartbeat to IP %s , port %d\n'
        'press Ctrl-C to stop\n') % (SERVER_IP, SERVER_PORT)
    hbSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    hbSocket.sendto('PyHB', (SERVER_IP, SERVER_PORT))
    lst = lstUDP(hbSocket)
    lst.setDaemon(True)
    lst.start()
    while True:
        hbSocket.sendto('PyHB', (SERVER_IP, SERVER_PORT))
    if __debug__: print 'Time: %s' % time.ctime()
    time.sleep(BEAT_PERIOD)

if __name__ == __main__:
    main()
