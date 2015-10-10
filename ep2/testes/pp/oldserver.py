#!/usr/bin/env python

# Filename: ThreadedBeatServer.py
"""Threaded heartbeat server"""

UDP_PORT = 43278; CHECK_PERIOD = 5; CHECK_TIMEOUT = 3;
TCP_PORT = 43278; MAX_TCP_CONNECT_QUEUE = 5;

import socket, threading, time, sys, select
from pprint import pprint

###Maquina de estados para o cliente###
def exit(cliente, args):
    print "encerrando conexao"
    if(cliente.connType == 'UDP'):
        cliente.connfd.sendto("EXIT\n", (cliente.ip, cliente.porta))
    else:
        cliente.connfd.sendall("EXIT\n");

def quit(cliente, args):
    print "saindo do jogo"

estados = {
    'CONECTADO': {'USER': None, 'NEWUSER': None, 'EXIT': exit },
    'LOGANDO': {'PASS': None, 'ABORT': quit, 'EXIT': exit },
    'LOGADO': {'PLAYACC': None, 'PLAYINV': None, 'PLAYDNY': None, 
               'LIST': None,'HALL': None, 'EXIT': exit },
    'REGISTRANDO': {'NEWNAME': None, 'NEWPASS': None, 'ABORT': None, 'EXIT': None },
    'ESPERANDO': { 'PLAYACC': None, 'ABORT': None, 'EXIT': exit },
    'JOGANDO': {'ABORT': quit, 'EXIT': exit },
}

###Classe com as informacoes da conexao###
class Cliente():
    def __init__(self, ip, porta, connType):
        self.ipTime = 0
        self.login = None
        self.connType = connType 
        self.ip = ip
        self.porta = porta
        self.connfd = None
        self.gameFile = None
        self.estado = "CONECTADO"
    
    def getMsg(self, msg):
        global estados
        msg = msg.split()
        cmd = msg[0]
        del msg[0]
        args = msg
        try:
            estados[self.estado][cmd](self, args)
        except KeyError:
            self.connfd.sendto("COMMAND %s INVALID!\n" % cmd, (self.ip, self.porta))
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
        silent = [(key, cliente) for (key, cliente) in self.items() if cliente.ipTime < limit]
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
                self.recSocket.sendto(data, addr)
                if not self.heartbeats.has_key((addr[0], addr[1])):
                    self.heartbeats[(addr[0],addr[1])] = Cliente(addr[0], addr[1], 'UDP')
                    self.heartbeats[(addr[0],addr[1])].connfd = self.recSocket 
                self.heartbeats[(addr[0], addr[1])].ipTime = time.time()
                self.heartbeats[(addr[0], addr[1])].getMsg(data)
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
                if not self.heartbeats.has_key((addr[0],addr[1])):
                    self.heartbeats[(addr[0],addr[1])] = Cliente(addr[0], addr[1], 'TCP')
                    self.heartbeats[(addr[0],addr[1])].connfd = cliSocket 
                    self.heartbeats[(addr[0],addr[1])].ipTime = time.time()
                    ConnTCP(connfd = cliSocket,
                        heartbeats = self.heartbeats, ip = addr[0],
                        porta = addr[1]).start()
                    
                else:
                    print "ERRO: ip ja esta no Dic"
                    cliSocket.sendall("ERRO: ip ja esta em uso\n")
                    cliSocket.shutdown(1)
                    cliSocket.close()

            except socket.timeout:
                pass

###ThreadTCP-CLI###                                                                                
class ConnTCP(threading.Thread):                                                           
    """Manage TCP connections"""                   
                                                                                               
    def __init__(self, connfd, heartbeats, ip, porta):
        super(ConnTCP, self).__init__()
        self.heartbeats = heartbeats
        self.recSocket = connfd
        self.ip = ip
        self.porta = porta
                                                                                               
    def run(self):                                                                             
        try:
            data = self.recSocket.recv(1024)
            while data != '':
                self.heartbeats[(self.ip, self.porta)].ipTime = time.time()
                self.recSocket.sendall('OK...' + data)
                data = self.recSocket.recv(1024)
                
        except socket.timeout:
            pass
###Thread do verificador de beats (feito no main)###
def main():
    receiverUDPEvent = threading.Event()
    receiverUDPEvent.set()
    
    receiverTCPEvent = threading.Event()
    receiverTCPEvent.set()
    
    hbUDP = Heartbeats()
    hbTCP = Heartbeats()
    
    #UDP#
    receiverUDP = ReceiverUDP(goOnEvent = receiverUDPEvent,
            heartbeats = hbUDP)
    receiverUDP.start()
# receiverUDP.setDaemon(True)
    print ('Threaded heartbeat server listening on port UDP %d\n'
        'press Ctrl-C to stop\n') % UDP_PORT
    
    
    #TCP#
    receiverTCP = ReceiverTCP(goOnEvent = receiverTCPEvent,
            heartbeats = hbTCP)
    receiverTCP.start()
#receiverTCP.setDaemon(True)
    print ('Threaded heartbeat server listening on port TCP %d\n'
        'press Ctrl-C to stop\n') % TCP_PORT
    
    try:
        while True:
            if select.select([sys.stdin,],[],[],0.0)[0]:
                print "\nTCP"
                pprint(hbTCP)
                print "\nUDP"
                pprint(hbUDP)
                raw_input()

            
            #UDP - Beats#
            silent = hbUDP.getSilent()
            print 'Silent clients UDP: %s' % silent
            for ip, cliente in silent:
                print '=>Silencioso ip: %s' % str(ip)
                cliente.connfd.sendto("Silencioso\n", (ip[0], ip[1]))
                del hbUDP[ip]

            #TCP - Beats#
            silent = hbTCP.getSilent()
            print 'Silent clientsTCP: %s' % silent
            for ip, cliente in silent:
                cliente.connfd.send("Silencioso\n")
                cliente.connfd.shutdown(1)
                cliente.connfd.close()
                del hbTCP[ip]
            time.sleep(CHECK_PERIOD)
    except KeyboardInterrupt:
        print 'Exiting, please wait...'
        receiverUDPEvent.clear()
        receiverTCPEvent.clear()
        receiverUDP.join()
        receiverTCP.join()
        print 'Finished.'

if __name__ == '__main__':
    main()
