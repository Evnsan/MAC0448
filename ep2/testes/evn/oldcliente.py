#!/usr/bin/env python

# Filename OldCliente.py

SERVER_PORTA = 8888; UDP_PORTA = 8886;

import socket, threading, time, sys, select

###TrheadUDP###
class ReceiverUDP(threading.Thread):
    """Receive UDP packets and log them in the heartbeats dictionary"""
                                                                                               
    def __init__(self, goOnEvent, socket, ip, porta):
        super(ReceiverUDP, self).__init__()
        self.goOnEvent = goOnEvent
        self.socket = socket
        self.ip = ip
        self.porta = porta
    def run(self):
        while self.goOnEvent.isSet():
            try:
                self.socket.sendto("PING\n", self.ip, self.porta)
            except socket.error:                                                             
                pass                                                                           
        self.recSocket.close()

def getLine():
    if select.select([sys.stdin,], [], [], 0.0)[0]:
        linha = raw_input() 
        return linha
    return None 

def main():
    if(len(sys.argv) < 2) :
        print "Modo de uso: ./oldcliente.py hostname\n"
        sys.exit()
    host = sys.argv[1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print socket.gethostbyname(host)
    s.bind((socket.gethostbyname(socket.gethostname()), UDP_PORTA))
    ip = socket.gethostbyname(host)
    s.sendto("USER evn", (socket.gethostbyname(host), SERVER_PORTA))
    while True:
        try:
            if select.select([sys.stdin,], [], [], 0.0)[0]:
                linha = raw_input() 
                s.sendto(linha,( ip, SERVER_PORTA))
            if select.select([s,], [], [], 0.0)[0]:
                data, addr = s.recvfrom(1024)
                print data
#time.sleep(1)
        except socket.error, msg:
            print "[ERRO] " + msg



if __name__ == '__main__':
    main()
