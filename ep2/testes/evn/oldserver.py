#!/usr/bin/env python

# Filename: ThreadedBeatServer.py
"""Threaded heartbeat server"""

UDP_PORT = 43278; CHECK_PERIOD = 10; CHECK_TIMEOUT = 8;
TCP_PORT = 43278; MAX_TCP_CONNECT_QUEUE = 5;

import socket, threading, time, sys, select
from pprint import pprint



###Funcoes auxiliares para as transicoes da maquina de estados
def teste(cliente, args, heartbeats):
    try:
        alvo = heartbeats.getList()
        cliente.send("LIST START\n")
        for username, est in alvo:
            cliente.send("%s "%username + est + "\n")
        cliente.send("LIST END\n")
    except IndexError, msg:
            cliente.send("[ERRO: TESTE] Argumentos Insuficientes\n")

def isPasswordCorrect(username, password):
    file = open('users', 'r')
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
        cliente.send("[ERRO NEWPASS->1] Comprimento da senha menor do que 3\n")
        return False
    
    if not password.isalnum():
        cliente.send("[ERRO NEWPASS->1] Password deve ter somente caracteres alfa-numericos\n")
        return False
    return True

def doesUserExist(username):
    file = open('users', 'r')

    for line in file:
        temp = line.split(';',1)
        print "primeiro token da linha no new user: " + temp[0]
        if(username == temp[0]):
            return True
    else:
        return False
    file.close()

###Maquina de estados para o cliente###
def exit(cliente, args, heartbeats):
    print "Encerrando sessao de %s:" % cliente.ip + str(cliente.porta) + " %s"% cliente.connType
    cliente.send("EXITING...\n")
    cliente.iptime = 0;
    cliente.estado = 'EXITING'

def user(cliente, args, heartbeats):
    #verificar se user existe
    #    pedir por password
    #    verificar se user e password estao corretos
    try:
        username = args[0]
        if doesUserExist(username):
            cliente.username = username
            cliente.estado = "LOGANDO"
        else:
            cliente.send("[ERRO: USER] Usuario Inexistente\n")
    except IndexError, msg:
            cliente.send("[ERRO: USER] Argumentos Insuficientes\n")

def abort_toConectado(cliente, args, heartbeats):
    cliente.username = None
    cliente.estado = "CONECTADO"

def newuser(cliente, args, heartbeats):
    #verificar se existe em um arquivo
    try:
        username = args[0]
        file = open('users', 'r')
    
        #se nao existe mudar para registrando
        if not doesUserExist(username):
            cliente.estado = "REGISTRANDO"
            cliente.username = args[0]
            cliente.send("USUARIO aceito\n")

        else:
            cliente.send("[ERROR NEWUSER] Ja exxiste usiario com este username\n")


        file.close()
    except IndexError, msg:
            cliente.send("[ERRO: NEWUSER] Argumentos Insuficientes\n")

def newpass(cliente, args, heartbeats):
    try:
        passValid = isValidPassword(cliente,args[0])

        if passValid:
            cliente.send("SENHA VALIDA\n")
            #escreve usuario e senha no arquivo
            file = open("users", "a+")
            file.write(cliente.username + ";" + args[0] + '\n')
            file.close()
            cliente.estado = "LOGADO"
            cliente.send("LOGADO! ENJOY\n")

        else:
            cliente.send("[ERRO: NEWPASS] Senha Invalida\n")
    except IndexError, msg:
            cliente.send("[ERRO: NEWPASS] Argumentos Insuficientes\n")

def checkpass(cliente, args, heartbeats):
    try:
        password = args[0]
        if isPasswordCorrect(cliente.username, password):
            cliente.estado = "LOGADO"
            cliente.send("LOGADO! ENJOY\n")
        else:
            cliente.send("[ERRO: PASS] Password Iconrreto!!\n")
    except IndexError, msg:
            cliente.send("[ERRO: PASS] Argumentos Insuficientes\n")

###Estados
estados = {
    'CONECTADO': {'USER': user, 'NEWUSER': newuser, 'EXIT': exit },
    'LOGANDO': {'PASS': checkpass, 'ABORT': abort_toConectado, 'EXIT': exit },
    'LOGADO': {'PLAYACC': None, 'PLAYINV': None, 'PLAYDNY': None, 
               'LIST': None,'HALL': None, 'EXIT': exit, 'ABORT': abort_toConectado, 'TESTE': teste },
    'REGISTRANDO': {'NEWNAME': None, 'NEWPASS': newpass, 'ABORT': abort_toConectado, 'EXIT': None },
    'ESPERANDO': { 'PLAYACC': None, 'ABORT': None, 'EXIT': exit },
    'JOGANDO': {'ABORT': quit, 'EXIT': exit },
}


###Classe com as informacoes da conexao###
class Cliente():
    def __init__(self, ip, porta, connType, flagTCP):
        self.ipTime = 0
        self.connType = connType
        self.flagTCP = flagTCP 
        self.ip = ip
        self.porta = porta
        self.connfd = None
        self.gameFile = None
        self.estado = "CONECTADO"
        self.username = None
        self.loginInvited = None
    
    def getMsg(self, msg, heartbeats):
        global estados
        msg = msg.split()
        cmd = msg[0]
        del msg[0]
        args = msg
        try:
            estados[self.estado][cmd](self, args, heartbeats)
        except KeyError:
            self.send("COMMAND %s INVALID!\n" % cmd)
    
    def send(self, msg):
        if(self.connType == 'UDP'):
            self.connfd.sendto(msg, (self.ip, self.porta))
        elif(self.connType == 'TCP'):
            self.connfd.sendall(msg)
 
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
    
    def getList(self):
        """Return a list of clients with heartbeat older than CHECK_TIMEOUT"""
        self._lock.acquire()
        retorno = []
        for (key, cliente) in self.items():
            if cliente.estado == 'LOGADO':
                est = "Disponivel"
                retorno.append((cliente.username, est))
            elif cliente.estado == 'ESPERANDO':
                est = "Iniciando partida"
                retorno.append((cliente.username, est))
            elif cliente.estado == 'JOGANDO':
                est = "Jogando"
                retorno.append((cliente.username, est))
        self._lock.release()
        return retorno
    
    def getClienteByName(self, name):
        """Retorna o cliente que tem atributo username = name ou None caso nao haja"""
        retorno = None
        self._lock.acquire()
        for (key, cliente) in self.items():
             if cliente.username == name:
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
                self.recSocket.sendto(data, addr) #somente Eco -> tirar
                if not self.heartbeats.has_key((addr[0], addr[1])):
                    self.heartbeats[(addr[0],addr[1])] = Cliente(addr[0], addr[1], 'UDP', None)
                    self.heartbeats[(addr[0],addr[1])].connfd = self.recSocket 
                if not self.heartbeats[addr].estado == 'EXITING': 
                    self.heartbeats[(addr[0], addr[1])].ipTime = time.time()
                    self.heartbeats[(addr[0], addr[1])].getMsg(data, self.heartbeats)
                else:
                    self.recSocket.sendto("Saindo. Por favor espere...\n", addr)
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
        while self.recSocket == None:
            try:
                self.recSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.recSocket.settimeout(CHECK_TIMEOUT)
                self.recSocket.bind(('', TCP_PORT))
                self.recSocket.listen(MAX_TCP_CONNECT_QUEUE)
            except socket.error, msg:
                self.recSocket = None
                sys.stderr.write("[ERRO] %s: Tentando novamente. Aguarde...\n" % msg[1])
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
                    print "[ERRO: CONNECT] ip+porta ja esta no Dic"
                    cliSocket.sendall("[ERRO: CONNECT] ip+porta ja esta em uso\n")
                    cliSocket.shutdown(socket.SHUT_RDWR)
                    cliSocket.close()

            except socket.timeout:
                pass
        print "Vai fechar o socket"
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
                if not self.heartbeats[(self.ip, self.porta)].estado == 'EXITING': 
                    self.heartbeats[(self.ip, self.porta)].ipTime = time.time()
                    self.heartbeats[(self.ip, self.porta)].getMsg(data, self.heartbeats)
                else:
                    self.recSocket.sendto("Saindo. Por favor espere...\n", addr)
            except KeyError, msg:
                sys.stderr.write("ERRO: ThreadTCPcli: KeyError = " + str(msg) + "\n")
            except socket.timeout:
                pass
        print "Matou uma Thread TCP-CLI"
###Thread do verificador de beats (feito no main)###
def main():
    receiverUDPEvent = threading.Event()
    receiverUDPEvent.set()
    
    receiverTCPEvent = threading.Event()
    receiverTCPEvent.set()
    
    hbUDP = Heartbeats()
    hbTCP = Heartbeats()

    open("users","a+").close()
    
    #UDP#
    receiverUDP = ReceiverUDP(goOnEvent = receiverUDPEvent,
            heartbeats = hbUDP)
    receiverUDP.start()
# receiverUDP.setDaemon(True)
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
                cliente.send("Silencioso\n")
                del hbUDP[ip]

            #TCP - Beats#
            silent = hbTCP.getSilent()
            print 'Silent clientsTCP: %s' % silent
            for ip, cliente in silent:
                try:
                    cliente.send("Silencioso\n")
                    cliente.connfd.shutdown(1)
                    cliente.connfd.close()
                except socket.error, msg:
                    sys.stderr.write("ERRO-  %s: Nao foi possivel fechar o socket\n")
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
