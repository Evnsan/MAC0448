#!/usr/bin/env python

# Filename: ThreadedBeatServer.py
"""Threaded heartbeat server"""

UDP_PORT = 43278; CHECK_PERIOD = 20; CHECK_TIMEOUT = 15
TCP_PORT = 43278; MAX_TCP_CONNECT_QUEUE = 5;

import socket, threading, time
###Classe com as informacoes da conexao###
class Estado():
    def __init__(self):
        self.ipTime = 0
        self.connfd = None
        self.gameFile = None
    
    def __str__(self):
        return str((str(self.ipTime) , str(self.connfd), str(self.gameFile)))

    def __repr__(self):
        return str((str(self.ipTime) , str(self.connfd), str(self.gameFile)))

##Dicionario de ip -> lastBeat###

class Heartbeats(dict):
    """Manage shared heartbeats dictionary with thread locking"""

    def __init__(self):
        super(Heartbeats, self).__init__()
        self._lock = threading.Lock()

    def __setitem__(self, key, value):
        """Create or update the dictionary entry for a client"""
        self._lock.acquire()
        super(Heartbeats, self).__setitem__(key, value)
        self._lock.release()

    def getSilent(self):
        """Return a list of clients with heartbeat older than CHECK_TIMEOUT"""
        limit = time.time() - CHECK_TIMEOUT
        self._lock.acquire()
        silent = [(ip, estado) for (ip, estado) in self.items() if estado.ipTime < limit]
        self._lock.release()
        return silent

###TrheadUDP###
class ReceiverUDP(threading.Thread):
    """Receive UDP packets and log them in the heartbeats dictionary"""

    def __init__(self, goOnEvent, heartbeats):
        super(ReceiverUDP, self).__init__()
        self.goOnEvent = goOnEvent
        self.heartbeats = heartbeats
        self.recSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.recSocket.settimeout(CHECK_TIMEOUT)
        self.recSocket.bind(('', UDP_PORT))

    def run(self):
        while self.goOnEvent.isSet():
            try:
                data, addr = self.recSocket.recvfrom(1024)
                if data == 'PyHB':
                    if not self.heartbeats.has_key(addr[0]):
                        self.heartbeats[addr[0]] = Estado()
                        self.heartbeats[addr[0]].connfd = None
                    self.heartbeats[addr[0]].ipTime = time.time()
            except socket.timeout:
                pass
###ThreadTCP###
class ReceiverTCP(threading.Thread):
    """Receive TCP connections and call thread ConnTCP to handle each one"""

    def __init__(self, goOnEvent, heartbeats):
        super(ReceiverTCP, self).__init__()
        self.goOnEvent = goOnEvent
        self.heartbeats = heartbeats
        self.recSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.recSocket.settimeout(CHECK_TIMEOUT)
        self.recSocket.bind(('', TCP_PORT))
        self.recSocket.listen(MAX_TCP_CONNECT_QUEUE)

    def run(self):
        while self.goOnEvent.isSet():
            try:
                cliSocket, addr = self.recSocket.accept()
                if not self.heartbeats.has_key(addr[0]):
                    self.heartbeats[addr[0]] = Estado()
                    self.heartbeats[addr[0]].connfd = cliSocket 
                    self.heartbeats[addr[0]].ipTime = time.time()
                else:
                    print "ERRO: ip ja esta no Dic"
                    cliSocket.send("ERRO: ip ja esta em uso\n")
                    cliSocket.shutdown(1)
                    cliSocket.close()

            except socket.timeout:
                pass


###Thread do verificador de beats (feito no main)###
def main():
    receiverUDPEvent = threading.Event()
    receiverUDPEvent.set()
    receiverTCPEvent = threading.Event()
    receiverTCPEvent.set()
    heartbeats = Heartbeats()
    
    receiverUDP = ReceiverUDP(goOnEvent = receiverUDPEvent,
            heartbeats = heartbeats)
    receiverUDP.start()
# receiverUDP.setDaemon(True)
    print ('Threaded heartbeat server listening on port UDP %d\n'
        'press Ctrl-C to stop\n') % UDP_PORT
    
    
    receiverTCP = ReceiverTCP(goOnEvent = receiverTCPEvent,
            heartbeats = heartbeats)
    receiverTCP.start()
#receiverTCP.setDaemon(True)
    print ('Threaded heartbeat server listening on port TCP %d\n'
        'press Ctrl-C to stop\n') % TCP_PORT
    
    try:
        while True:
            silent = heartbeats.getSilent()
            print 'Silent clients: %s' % silent
            time.sleep(CHECK_PERIOD)
            for ip, estado in silent:
                print 'ip = %s e estado = %s' % ip ,estado
    except KeyboardInterrupt:
        print 'Exiting, please wait...'
        receiverUDPEvent.clear()
        receiverTCPEvent.clear()
        receiverUDP.join()
        receiverTCP.join()
        print 'Finished.'

if __name__ == '__main__':
    main()
