#!/usr/bin/env python

# Filename OldCliente.py

SERVER_TCP_PORTA = 8888; SERVER_UDP_PORTA = 8888;
UDP_PORTA = 8886; TCP_PORTA = 8886;
TIME_BEAT = 10;

import socket, threading, time, sys, select

##############################################################################
def ok(link, msg):
    print "[SERVER OK] " + str(msg)

def cmdList(link, msg):
    print "[SERVER CMDS] " + str(msg) 

def ping(link, msg):
    print "[SERVER PING] " + str(msg)

def exit(link, msg):
    link.goOnEvent.clear() 

def invalidcmd(link, msg):
    print "Comando invalido " + str(msg[0])

def listStart(link, msg):
    try:
        if msg[0] == START:
            link.estado = 'LISTANDO'
    except IndexError, msg:
        print "[LISTSTART] " + str(msg)

def listStop(link, msg):
    try:
        if msg[0] == START:
            link.estado = 'CONECTADO'
    except IndexError, msg:
        print "[LISTSTOP] " + str(msg)

def listar(link, msg):
    print str(msg[0]) + str(msg[1])

##############################################################################

###Estado do Cliente##########################################################
estados = {
    'CONECTADO': {'OK': ok, 'EXITING': exit, 'CMDLIST': cmdList,
                  'PING': ping, 'INVALIDCMD': invalidcmd},

    'LOGANDO': {'OK': ok, 'EXITING': exit, 'CMDLIST': cmdList, 'PING': ping},

    'LOGADO': {'OK': ok, 'EXITING': exit, 'CMDLIST': cmdList, 'PING': ping,
               'LIST': listStart},
    
    'LISTANDO': {'LL': listar, 'EXITING': exit, 'CMDLIST': cmdList,
                 'PING': ping, 'LIST':listStop },

    'REGISTRANDO': {'OK': ok, 'EXITING': exit, 'CMDLIST': cmdList,
                    'PING': ping},

    'ESPERANDO': {'OK': ok, 'EXITING': exit, 'CMDLIST': cmdList,
                  'PING': ping},

    'JOGANDO_WAIT': {'OK': ok, 'EXITING': exit, 'CMDLIST': cmdList,
                     'PING': ping},

    'JOGANDO_PLAY': {'OK': ok, 'EXITING': exit, 'CMDLIST': cmdList,
                     'PING': ping},
}
##############################################################################

###Funcoes Auxiliares#########################################################
def getLine():
    if select.select([sys.stdin,], [], [], 0.0)[0]:
        linha = raw_input() 
        return linha
    return None 
##############################################################################

###Link#######################################################################
class Link():
    def __init__(self, socket, ip, porta, protocolo, goOnEvent):
        self._lock = threading.Lock()
        self.socket = socket
        self.ip = ip
        self.porta = porta
        self.protocolo = protocolo
        self.goOnEvent = goOnEvent
        self.estado = 'CONECTADO'

    def getLine(self):
        linha = None
        if self.goOnEvent.isSet():
            self._lock.acquire()
            if select.select([self.socket], [], [], 0.0)[0]:
                if self.protocolo == 'UDP':
                    linha, addr = self.socket.recvfrom(1024)
                elif self.protocolo == 'TCP':
                    linha = self.socket.recv(1024)
                self.getMsg(linha)
            self._lock.release()
        return linha

    def send(self, msg):
        self._lock.acquire()
        if self.goOnEvent.isSet():
            if self.protocolo == 'UDP':
                self.socket.sendto(msg, (self.ip, self.porta))
            elif self.protocolo == 'TCP':
                self.socket.sendall(msg)
            self._lock.release()

    def close(self):
        if self.protocolo == 'UDP':
            self.socket.close()
        elif self.protocolo == 'TCP':
            print "vai fechar"
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()

    def getMsg(self, msg):
        global estados
        msg = msg.split()
        if len(msg) > 0:
            cmd = msg[0]
            del msg[0]
            args = msg
            try:
                estados[self.estado][cmd](self, args)
            except KeyError, erro:
               print "[LINK GETMSG] " + str(erro)  
               print "[LINK GETMSG] " + str(cmd) + " " + str(args)  
##############################################################################

###TrheadUDP##################################################################
class ThreadUDP(threading.Thread):
    """Receive UDP packets and log them in the heartbeats dictionary"""
    
    def __init__(self, goOnEvent, link):
        super(ThreadUDP, self).__init__()
        self.goOnEvent = goOnEvent
        self.link = link
    def run(self):
        while self.goOnEvent.isSet():
            try:
                linha = getLine()
                if linha != None: 
                    self.link.send(linha)
                linha = self.link.getLine()
                if linha != None: 
                    linha = linha.split('\n', 2)[0]
                    if linha == 'EXITING...':
                        self.goOnEvent.clear()
                    print linha
                #time.sleep(1)
            except socket.error, msg:
                print "[THREADUDP] " + msg
                pass
        self.link.close()
##############################################################################

###ThreadTCP##################################################################
class ThreadTCP(threading.Thread):
    """Receive TCP connections and call thread ConnTCP to handle each one"""

    def __init__(self, goOnEvent, link):
        super(ThreadTCP, self).__init__()
        self.goOnEvent = goOnEvent
        self.link = link

    def run(self):
        while self.goOnEvent.isSet():
            try:
                linha = getLine()
                if linha != None: 
                    self.link.send(linha)
                linha = self.link.getLine()
                if linha != None: 
                    linha = linha.split('\n', 2)[0]
                    if linha == 'EXITING...':
                        self.goOnEvent.clear()
                    print linha
                #time.sleep(1)
            except socket.error, msg:
                print "[THREADTCP] " + msg
                pass
        self.link.close()
##############################################################################

##############################################################################

###Main#######################################################################
def main():
    if(len(sys.argv) < 3) :
        print "Modo de uso: ./oldcliente.py HOSTNAME TCP|UDP [PORTA]\n"
        sys.exit(0)
    ##declaracoes inicias##
    goOnEvent = threading.Event()
    goOnEvent.set()

    ipServer = socket.gethostbyname(sys.argv[1])
    protocolo = sys.argv[2]
    ####UDP####
    if(protocolo == 'UDP' or protocolo == 'udp' or protocolo == 'Udp'):
        try:
            porta = int(sys.argv[3])
        except IndexError:
            porta = UDP_PORTA
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('', porta))
        link = Link(socket = s, ip = ipServer, porta = SERVER_UDP_PORTA,
                    protocolo = 'UDP', goOnEvent = goOnEvent)
        link.send("PING\n")
        threadUDP = ThreadUDP(goOnEvent = goOnEvent, link = link)
        threadUDP.start()
        while goOnEvent.isSet():
            try:
                link.send("PING\n")
                time.sleep(TIME_BEAT)
            except socket.error, msg:
                print "[ERRO] " + str(msg)
            except KeyboardInterrupt:
                print "[MAIN] Encerrando Server..."
                goOnEvent.clear() 
                threadUDP.join()
                print "[MAIN] Encerrado"
                sys.exit(0)
    ###########
    ####TCP####             
    elif(protocolo == 'TCP' or protocolo == 'tcp' or protocolo == 'Tdp'):
        try:
            porta = int(sys.argv[3])
        except IndexError:
            porta = UDP_PORTA
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ipServer, SERVER_TCP_PORTA))
        except socket.error, msg:
            print "[ERRO MAIN] " + str(msg)
            s.close()
            sys.exit(0)
        link = Link(socket = s, ip = ipServer, porta = SERVER_TCP_PORTA,
                    protocolo = 'TCP', goOnEvent = goOnEvent)
        link.send("PING\n")
        threadTCP = ThreadTCP(goOnEvent = goOnEvent, link = link)
        threadTCP.start()
        while goOnEvent.isSet():
            try:
                link.send("PING\n")
                time.sleep(TIME_BEAT)
            except socket.error, msg:
                print "[ERRO] " + str(msg)
            except KeyboardInterrupt:
                print "[MAIN] Encerrando Server..."
                goOnEvent.clear() 
                threadTCP.join()
                print "[MAIN] Encerrado"
                sys.exit(0)
    ###########
    else:
        print "[ERRO OLDCLIENTE] Argumento informado nao foi nem TCP nem UDP"
        sys.exit(0)

##############################################################################
if __name__ == '__main__':
    main()
##############################################################################
