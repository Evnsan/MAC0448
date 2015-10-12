#!/usr/bin/env python

# Filename: ThreadedBeatServer.py
"""Threaded heartbeat server"""

UDP_PORT = 43278; CHECK_PERIOD = 5; CHECK_TIMEOUT = 3;
TCP_PORT = 43278; MAX_TCP_CONNECT_QUEUE = 5;

import socket, threading, time, sys, select
from pprint import pprint



###Funcoes auxiliares para as transicoes da maquina de estados

def isPasswordCorrect(username, password):                                     
    file = open('users', 'r');                                                 
    print 'checando se password esta correto'                                  
    for line in file:                                                          
        temp = line.split(';',2)                                               
        pws = temp[1].split('\n',1)                                            
        if username == temp[0]:                                                
            print 'encontrou usuario e vai tentar ver se a senha esta correta' 
            if pws[0] == password:                                             
                file.close()                                                   
                return True                                                    
            else:                                                              
                file.close()                                                   
                return False                                                   
                                                                               
    file.close()                                                               
    return False

def isValidPassword(cliente, password):
    if len(password) < 3:
        cliente.connfd.sendto("comprimento menor que 3 da senha\n", (cliente.ip, cliente.porta))
        return False
    
    if not password.isalnum():
        cliente.connfd.sendto("PASS deve ter somente alfa-numericos\n", (cliente.ip, cliente.porta))
        return False
    return True

def doesUserExist(username):
    file = open('users', 'r');

    for line in file:
        temp = line.split(';',1)
        print "primeiro token da linha no new user: "+ temp[0];
        if(username == temp[0]):
            return True
    else:
        return False
    file.close()

###Rotina dos comandos###
def exit(cliente, args):
    print "encerrando conexao"
    if(cliente.connType == 'UDP'):
        cliente.connfd.sendto("EXITING...\n", (cliente.ip, cliente.porta))
        cliente.iptime = 0
        cliente.estado = "EXITING"
    else:
        cliente.connfd.sendall("EXITING...\n");
        cliente.iptime = 0
        cliente.estado = "EXITING"

def quit(cliente, args):
    print "saindo do jogo"

def user(cliente, args):                                                       
    #verificar se user existe                                                  
    #    pedir por password                                                    
    #    verificar se user e password estao corretos                           
    username = args[0]                                                         
    if doesUserExist(username):                                                
        cliente.username = username                                            
        cliente.estado = "LOGANDO"                                             
    else:                                                                      
        cliente.connfd.sendto("USUARIO NAO EXISTE\n", (cliente.ip, cliente.porta))

def newuser(cliente, args):
    #verificar se existe em um arquivo
    username = args[0]
    file = open('users', 'r');
    
    #se nao existe mudar para registrando
    if not doesUserExist(username):
        cliente.estado = "REGISTRANDO"
        cliente.username = args[0]
        cliente.connfd.sendto("USUARIO aceito\n", (cliente.ip, cliente.porta))

    else:
        cliente.connfd.sendto("USUARIO JA EXISTE\n", (cliente.ip, cliente.porta))


    file.close()

def abort_registrando(cliente, args):
    cliente.estado = "CONECTADO"

def newpass(cliente, args):
    passValid = isValidPassword(cliente,args[0])

    if passValid:
        cliente.connfd.sendto("SENHA VALIDA\n", (cliente.ip, cliente.porta))

        cliente.password = args[0]
        #escreve usuario e senha no arquivo
        file = open("users", "a+")
        file.write(cliente.username + ";" +cliente.password + '\n')
        file.close()
        cliente.estado = "LOGADO"
        cliente.connfd.sendto("LOGADO! ENJOY\n", (cliente.ip, cliente.porta))

    else:
        cliente.connfd.sendto("SENHA INVALIDA\n", (cliente.ip, cliente.porta))

def checkpass(cliente, args):                                                  
    password = args[0]                                                         
    cliente.connfd.sendto(password, (cliente.ip, cliente.porta))               
    if isPasswordCorrect(cliente.username, password):                          
        cliente.estado = "LOGADO"                                              
        cliente.connfd.sendto("LOGADO! ENJOY\n", (cliente.ip, cliente.porta))  
    else:                                                                      
        cliente.connfd.sendto("PASSWORD INCORRETO!!\n", (cliente.ip, cliente.porta))

###Maquina de estados para o cliente###
estados = {
    'CONECTADO': {'USER': user, 'NEWUSER': newuser, 'EXIT': exit },
    'LOGANDO': {'PASS': checkpass, 'ABORT': quit, 'EXIT': exit },
    'LOGADO': {'PLAYACC': None, 'PLAYINV': None, 'PLAYDNY': None, 
               'LIST': None,'HALL': None, 'EXIT': exit },
    'REGISTRANDO': {'NEWNAME': None, 'NEWPASS': newpass, 'ABORT': abort_registrando, 'EXIT': None },
    'ESPERANDO': { 'PLAYACC': None, 'ABORT': None, 'EXIT': exit },
    'JOGANDO': {'ABORT': quit, 'EXIT': exit },
    'EXITING': {},
}


###Classe com as informacoes da conexao###
class Cliente():
    def __init__(self, ip, porta, connType, flagTCP):
        self._lock = threading.Lock()
        self.ipTime = 0
        self.connType = connType
        self.flagTCP = flagTCP 
        self.ip = ip
        self.porta = porta
        self.connfd = None
        self.gameFile = None
        self.estado = "CONECTADO"
        self.username = None
        self.adversario = None

    def getMsg(self, msg, heartbeats):
        global estados
        msg = msg.split()
        cmd = msg[0]
        del msg[0]
        args = msg
        try:
            estados[self.estado][cmd](self, args, heartbeats)
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

    def __detitem__(self, key):
        """Create or update the dictionary entry for a client"""
        self._lock.acquire()
        if key not in self:
            raise KeyError(str(key))
        super(Heartbeats, self).__detitem__(key)
        self._lock.release()

    def getSilent(self):
        """Return a list of clients with heartbeat older than CHECK_TIMEOUT"""
        limit = time.time() - CHECK_TIMEOUT
        self._lock.acquire()
        silent = [(key, cliente) for (key, cliente) in self.items() if cliente.ipTime < limit]
        self._lock.release()
        return silent
    
    def getClienteByName(selfi, username):
        """Return a list of clients with heartbeat older than CHECK_TIMEOUT"""
        self._lock.acquire()
        retorno = None
        for key, cliente in self.items():
             if cliente.getUsername == username:
                retorno = cliente
        self._lock.release()
        return retorno

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
                    self.heartbeats[(addr[0],addr[1])] = Cliente(addr[0], addr[1], 'UDP', None)
                    self.heartbeats[(addr[0],addr[1])].connfd = self.recSocket 
#if self.heartbeats[add].estado != "EXITING": 
                self.heartbeats[(addr[0], addr[1])].ipTime = time.time()
                self.heartbeats[(addr[0], addr[1])].getMsg(data, self.heatbeats)
            except socket.timeout:
                pass
        self.recSocket.close()
###ThreadTCP###
class ReceiverTCP(threading.Thread):
    """Receive TCP connections and call thread ConnTCP to handle each one"""

    def __init__(self, goOnEvent, heartbeats):
        super(ReceiverTCP, self).__init__()
        self.goOnEvent = goOnEvent
        self.heartbeats = heartbeats
        self.recSocket = None
        while self.recSocket == None and self.goOnEvent.isSet():
            try:
                self.recSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.recSocket.settimeout(CHECK_TIMEOUT)
                self.recSocket.bind(('', TCP_PORT))
                self.recSocket.listen(MAX_TCP_CONNECT_QUEUE)
                print self.recSocket
            except socket.error, msg:
                self.recSocket = None
                sys.stderr.write("[ERROR] %s : Tentando Novamente, Aguarde\n" % msg[1])
                time.sleep(1)
            
    def run(self):
        while self.goOnEvent.isSet():
            try:
                cliSocket, addr = self.recSocket.accept()
                if not self.heartbeats.has_key((addr[0],addr[1])):
                    flagTCP = threading.Event()
                    flagTCP.set() 
                    self.heartbeats[(addr[0],addr[1])] = Cliente(addr[0], addr[1], 'TCP', flagTCP)
                    self.heartbeats[(addr[0],addr[1])].connfd = cliSocket 
                    self.heartbeats[(addr[0],addr[1])].ipTime = time.time()
                    ConnTCP(connfd = cliSocket,
                        heartbeats = self.heartbeats, ip = addr[0],
                        porta = addr[1], goOnEvent = flagTCP).start()
                    
                else:
                    print "ERRO: ip ja esta no Dic"
                    cliSocket.sendall("ERRO: ip ja esta em uso\n")
                    cliSocket.shutdown(1)
                    cliSocket.close()

            except socket.timeout:
                pass
        print "Vai fechar o socket ReceiverTCP"
        self.recSocket.close()

###ThreadTCP-CLI###                                                                                
class ConnTCP(threading.Thread):                                                           
    """Manage TCP connections"""                   
                                                                                               
    def __init__(self, connfd, heartbeats, ip, porta, goOnEvent):
        super(ConnTCP, self).__init__()
        self.goOnEvent = goOnEvent
        self.heartbeats = heartbeats
        self.recSocket = connfd
        self.ip = ip
        self.porta = porta
                                                                                               
    def run(self):                                                                             
        while self.goOnEvent.isSet():
            try:
                data = self.recSocket.recv(1024)
                if data != '':
                    self.heartbeats[(self.ip, self.porta)].ipTime = time.time()
                    self.recSocket.sendall('OK...' + data)
                else:
                    print self.ip
                    print self.porta
            except socket.timeout:
                pass
        print "Matou uma Thread TCP-CLI %s" % self
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
    print ('Threaded heartbeat server listening on port UDP %d\n'
        'press Ctrl-C to stop\n') % UDP_PORT
    
    
    #TCP#
    try:
        receiverTCP = ReceiverTCP(goOnEvent = receiverTCPEvent,
            heartbeats = hbTCP)
        receiverTCP.start()
    except KeyboardInterrupt, msg:
        sys.stderr.write("Server interrompido...\n")
        receiverUDPEvent.clear()
        receiverUDP.join()
        sys.stderr.write("Finalizado\n")
        sys.exit(1)
    except Exception, msg:
        receiverUDPEvent.clear()
        receiverUDP.join()
        sys.stderr.write("[ERROR] %s\n" % msg)
        sys.exit(1)

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
                cliente.flagTCP.clear()
                del hbTCP[ip]
            time.sleep(CHECK_PERIOD)
    except KeyboardInterrupt:
        print 'Exiting, please wait...'
        receiverUDPEvent.clear()
        receiverTCPEvent.clear()
        for ip in hbTCP:
            hbTCP[ip].flagTCP.clear()
            hbTCP[ip].connfd.close()
        receiverUDP.join()
        receiverTCP.join()
        print 'Finished.'

if __name__ == '__main__':
    main()
