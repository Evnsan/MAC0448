#!/usr/bin/env python

# Filename: OldServer.py

UDP_PORT = 8888; CHECK_PERIOD = 30; CHECK_TIMEOUT = 25;
TCP_PORT = 8888; MAX_TCP_CONNECT_QUEUE = 5;

import socket, threading, time, sys, select
from pprint import pprint


###Funcoes auxiliares para as transicoes da maquina de estados

def isPasswordCorrect(username, password):
    f = open('users', 'r')
    print 'checando se password esta correto'
    for line in f:
        temp = line.split(';',2)
        pws = temp[1].split('\n',1)
        if username == temp[0]:
            print 'encontrou usuario e vai tentar ver se a senha esta correta'
            if pws[0] == password:
                f.close()
                return True
            else:
                f.close()
                return False

    f.close()
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
    f = open('users', 'r')

    for line in f:
        temp = line.split(';',1)
        if(username == temp[0]):
            return True
    else:
        return False
    f.close()

###Maquina de estados para o cliente###


def caniplay(cliente, args, heartbeats):
    try:
        f = open(cliente.gamefilename,"r")
        if f.readline() == cliente.username + "\n":
            cliente.estado = "JOGANDO_PLAY"
            cliente.send("CANIPLAY OK\n")
        else:
            cliente.send("CANIPLAY NO\n")
        f.close()    
    except IOError, msg:
        sys.stderr.write("[ERRO CANIPLAY] %s"%msg +"\n")

def carregaTabuleiro(filename):
    try:
        f = open(filename, "r")
        f.readline()
        return f.readline()
    except IOError, msg:
        sys.stderr.write("[ERRO CARREGATABULEIRO] %s"%msg +"\n")

def realizaJogada(coordenada, tabuleiro, classe):
    teste = tabuleiro.split("\n")
    teste = teste[0].split(" ")
    retorno = ""
    try:
        print str(teste)
        print teste[int(coordenada)]
        if teste[int(coordenada)] == '0':
            teste[int(coordenada)] = str(classe)
            retorno = teste[0]
            for i in range(1,9):
                retorno = retorno + " " + teste[i]
            print retorno
            return retorno
        else:
            return None
    except IndexError, msg:
            sys.stderr.write("[ERRO REALIZAJOGADA] Cordenada %s Invalida"%coordenada)
    return None
        
def play(cliente, args, heartbeats):
    try:
        cordenada = args[0]
        tabuleiro = carregaTabuleiro(cliente.gamefilename)#verifica se jogada eh valida
        print "tabuleiro: " + tabuleiro
        novoTabuleiro = realizaJogada(cordenada, tabuleiro, cliente.gameclasse)
        if novoTabuleiro:
            f = open(cliente.gamefilename,"w")
            f.write(cliente.adversario + '\n')
            f.write(novoTabuleiro + '\n')
            cliente.send("BOARD " + novoTabuleiro + '\n')
            cliente.estado = "JOGANDO_WAIT"
            #confere tabuleiro
            #se nao acabou
                #muda estado do jogador
                #manda mensagem para o proximo jogador
                #envia novo tabuleiro para ambos
            #se acabou
                #modifica pontuacao
                #muda estado
                #manda mensagem pros jogadores
        else:
            cliente.send("[ERRO PLAY] Cordenada %s Invalida"%cordenada)

    except IndexError, msg:
        cliente.send("[ERRO PLAY] Argumentos Insuficientes\n")

def playinv(cliente, args, heartbeats):
    try:
        playerToInvite = args[0]
        chatporta = args[1]
        clienteToInvite = heartbeats.getClienteByName(playerToInvite)
        if clienteToInvite:
            clienteToInvite.send("PLAYINV "+ cliente.username + " " + chatporta + "\n")
            cliente.estado = "ESPERANDO"
            cliente.adversario = clienteToInvite.username
        else:
            cliente.send("[ERRO: PLAYINV] Usuario nao esta onlinen\n")
    except IndexError, msg:
        cliente.send("[ERRO: PLAYINV] Argumentos Insuficientes\n")

def listingStates(estado):
        if estado == "JOGANDO":
            return True
        if estado == "ESPERANDO":
            return True
        if estado == "LOGADO":
            return True
        if cliente.estado == "PRONTO":
            return True
        return False

def listPlayers(cliente, args, heartbeats):
    try:
        alvo = heartbeats.getList()
        cliente.send("LIST START\n")
        for username, est in alvo:
            cliente.send("LL " + username + " " + est + "\n")
        cliente.send("LIST END\n")
    except IndexError, msg:
            cliente.send("[ERRO: LISTPLAYERS] Argumentos Insuficientes\n")

def playacc_esperando(cliente, args, heartbeats):
    #esperando_jogo
    
    try:
        usernameAdv = args[0]
        chatporta = args[1]
        cliente.estado = "JOGANDO_WAIT"
        if cliente.adversario == usernameAdv:
            pontos = None
            try:
                f = open(cliente.username, "r")
                pontos = f.readline()
                f.close()
            except IOError, msg:
                print "blah\n"
            f = open(cliente.username, "w")
            if pontos:
                f.write(pontos)
            else:
                f.write("0\n")
            cliente.gamefilename = usernameAdv+cliente.username
            cliente.gameclasse = 2
            f.write('JOGANDO\n')
            f.write(usernameAdv + '\n') 
            f.write('SERVER\n')     
            f.write(chatporta + '\n')     
            f.write('2\n')
            f.write(cliente.gamefilename + '\n') 
            f.close()
            cliente.send("SEU CONVITE FOI ACEITO, VOCE ESTA EM UM JOGO!\n")
      
    except IndexError, msg:
        cliente.send("[ERRO: PLAYACC_ESPERANDO] Argumentos Insuficientes\n")

def playacc_logado(cliente, args, heartbeats):
    try:
        usernameAdv = args[0]
        chatporta = args[1]
        clienteToPlay = heartbeats.getClienteByName(usernameAdv)
        cliente.estado = "JOGANDO_PLAY"
        cliente.adversario = usernameAdv
        cliente.gamefilename = cliente.username+usernameAdv
        cliente.adversario = usernameAdv
        cliente.gameclasse = 1

        f2 = open(cliente.gamefilename, "w")
        f2.write(cliente.username + '\n')
        f2.write('0 0 0 0 0 0 0 0 0\n')                
        f2.close()
        if not clienteToPlay is None:

            if clienteToPlay.adversario == cliente.username:
                pontos = None
                try:
                    f = open(cliente.username, "r")
                    
                    pontos = f.readline()
                    f.close()
                except IOError, msg:
                    print "[WARNING PLAYACC_LOGADO] Cliente nao tinha file\n"
                f = open(cliente.username, "w")
                if pontos:
                    f.write(pontos)
                else:
                    f.write("0\n")
                
                f.write('JOGANDO\n')
                f.write(usernameAdv + '\n')                                                                          
                f.write('CLIENTE\n')
                f.write(chatporta + '\n')
                f.write('1\n')
                f.write(cliente.gamefilename + '\n')    
                f.close()

                cliente.send("VOCE ACEITOU O CONVITE E AGORA ESTA EM UM JOGO!\n")
                clienteToPlay.send("PLAYACC " + cliente.username + " " + chatporta + "\n")
            else:
                cliente.send("[ERRO: PLAYACC_LOGADO]  Usuario %s nao esta convidando\n"%usernameAdv)
        else:
            cliente.send("[ERRO: PLAYACC_LOGADO] Usuario nao esta online\n")   
    except IndexError, msg:
        cliente.send("[ERRO: PLAYACC_LOGADO] Argumentos Insuficientes\n")             

def exit(cliente, args, heartbeats):
    ip = heartbeats.getKeyForCliente(cliente)
    cliente.estado = 'EXITING'
    del heartbeats[ip]
    cliente.exit()

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

def abort_esperando(cliente, args, heartbeats):
    cliente.adversario = None
    cliente.estado = "LOGADO"

def playdny(cliente, args, heartbeats):
    try:
        inviter = heartbeats.getClienteByName(args[0])
        if(inviter.adversario == cliente.username):
            inviter.send("PLAYDNY %s\n"%cliente.username)
    except IndexError, msg:
        cliente.send("[ERRO PLAYDNY] Argumentos Insuficientes\n")

def newuser(cliente, args, heartbeats):
    #verificar se existe em um arquivo
    try:
        username = args[0]
        f = open('users', 'r')
    
        #se nao existe mudar para registrando
        if not doesUserExist(username):
            cliente.estado = "REGISTRANDO"
            cliente.username = args[0]
            cliente.send("USUARIO aceito\n")

        else:
            cliente.send("[ERROR NEWUSER] Ja exxiste usiario com este username\n")


        f.close()
    except IndexError, msg:
            cliente.send("[ERRO: NEWUSER] Argumentos Insuficientes\n")

def newpass(cliente, args, heartbeats):
    try:
        passValid = isValidPassword(cliente,args[0])

        if passValid:
            cliente.send("SENHA VALIDA\n")
            #escreve usuario e senha no arquivo
            f = open("users", "a+")
            f.write(cliente.username + ";" + args[0] + '\n')
            f.close()
            cliente.estado = "LOGADO"
            cliente.send("LOGADO\n")

        else:
            cliente.send("[ERRO: NEWPASS] Senha Invalida\n")
    except IndexError, msg:
            cliente.send("[ERRO: NEWPASS] Argumentos Insuficientes\n")

def checkpass(cliente, args, heartbeats):
    try:
        password = args[0]
        if isPasswordCorrect(cliente.username, password):
            cliente.estado = "LOGADO"
            cliente.send("LOGADO\n")
        else:
            cliente.send("[ERRO: PASS] Password Iconrreto!!\n")
    except IndexError, msg:
            cliente.send("[ERRO: PASS] Argumentos Insuficientes\n")

def board(cliente, args, heartbeats):
    tabuleiro = carregaTabuleiro(cliente.gamefilename)
    cliente.send("BOARD " + tabuleiro)
    
def cmdInvalido(cliente, args, heartbeats):
    cliente.send("[ERRO CMDINVALIDO] Comando invalido para o estado %s\n"%cliente.estado)

def cmdList(cliente, args, heartbeats):
    msg0 = "CMDLIST %s: "%cliente.estado
    msg = {
        'CONECTADO':  "USER, NEWUSER, CMDLIST, EXIT\n",
        'LOGANDO': "PASS, ABORT, CMDLIST, EXIT\n",
        'LOGADO': "PLAYACC, PLAYINV, PLAYDNY, LIST, HALL, ABORT, CMDLIST, EXIT\n",
        'REGISTRANDO': "NEWNAME, NEWPASS, ABORT, CMDLIST, EXIT\n",
        'ESPERANDO': "PLAYACC, ABORT, CMDLIST, EXIT\n",
        'JOGANDO_WAIT': "ABORT, BOARD, CANIPLAY, CMDLIST, EXIT\n",
        'JOGANDO_PLAY': "ABORT, BOARD, PLAY, CMDLIST, EXIT\n" }
    cliente.send(msg0 + msg[cliente.estado])

def ping(cliente, args, heartbeats):
    pass

###Estados
estados = {
    'CONECTADO': {'USER': user, 'NEWUSER': newuser, 'ABORT': cmdInvalido, 'EXIT': exit,
                  'CMDLIST': cmdList, 'PING': ping},

    'LOGANDO': {'PASS': checkpass, 'ABORT': abort_toConectado, 'EXIT': exit,
                'CMDLIST': cmdList, 'PING': ping},

    'LOGADO': {'PLAYACC': playacc_logado, 'PLAYINV': playinv, 'PLAYDNY': playdny, 
               'LIST': listPlayers,'HALL': None, 'EXIT': exit, 'ABORT': abort_toConectado,
               'CMDLIST': cmdList, 'PING': ping},

    'REGISTRANDO': {'NEWNAME': None, 'NEWPASS': newpass, 'ABORT': abort_toConectado,
               'EXIT': exit, 'CMDLIST': cmdList, 'PING': ping},

    'ESPERANDO': {'PLAYACC': playacc_esperando, 'ABORT': abort_esperando, 'EXIT': exit,
               'CMDLIST': cmdList, 'PING': ping},

    'JOGANDO_WAIT': {'ABORT': None, 'BOARD': board, 'EXIT': exit , 'CANIPLAY': caniplay,
               'CMDLIST': cmdList, 'PING': ping},

    'JOGANDO_PLAY': {'ABORT': None, 'BOARD': board, 'EXIT': exit, 'PLAY': play,
               'CMDLIST': cmdList, 'PING': ping},
}


##Classe com as informacoes da conexao###
class Cliente():
    def __init__(self, ip, porta, connType, flagTCP):
        self.ipTime = 0
        self.connType = connType
        self.flagTCP = flagTCP 
        self.ip = ip
        self.porta = porta
        self.connfd = None
        self.gamefilename = None
        self.gameclasse = None
        self.estado = "CONECTADO"
        self.username = None
        self.adversario = None
    
    def getMsg(self, msg, heartbeats):
        global estados
        msg = msg.split()
        if len(msg) > 0:
            cmd = msg[0]
            del msg[0]
            args = msg
            try:
                estados[self.estado][cmd](self, args, heartbeats)
            except KeyError:
                self.send("INVALIDCMD %s\n" % cmd)

    def exit(self):
        print "Encerrando sessao de %s:" % self.ip + str(self.porta) + " %s"% self.connType
        msg = "EXITING\n"
        if(self.connType == 'UDP'):
            self.connfd.sendto(msg, (self.ip, self.porta))
        elif(self.connType == 'TCP'):
            self.connfd.sendall(msg)
            try:
                self.connfd.shutdown(socket.SHUT_RDWR)
                self.connfd.close()
            except socket.error, msg:
                sys.stderr.write("ERRO-  %s: Nao foi possivel fechar o socket\n")
    
    def send(self, msg):
        if(self.connType == 'UDP'):
            self.connfd.sendto(msg, (self.ip, self.porta))
        elif(self.connType == 'TCP'):
            self.connfd.sendall(msg)
 
    def __str__(self):
        return str((str(self.ipTime) , str(self.connfd), str(self.gamefilename)))

    def __repr__(self):
        return str((str(self.ipTime) , str(self.connfd), str(self.gamefilename)))

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
            elif cliente.estado == 'JOGANDO_PLAY' or cliente.estado == 'JOGANDO_PLAY':
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
    
    def getKeyForCliente(self, entrada):
        """Retorna a chave "(ip:porta)" do cliente"""
        retorno = None
        self._lock.acquire()
        for (key, cliente) in self.items():
             if cliente == entrada:
                retorno = key
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
                if data != '':
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
                self.recSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
                if not self.heartbeats[(self.ip, self.porta)].estado == 'EXITING': 
                    self.heartbeats[(self.ip, self.porta)].ipTime = time.time()
                    self.heartbeats[(self.ip, self.porta)].getMsg(data, self.heartbeats)
                    if self.heartbeats[(self.ip, self.porta)].estado == 'EXITING':
                        self.goOnEvent.clear()
                else:
                    self.recSocket.sendall("Saindo. Por favor espere...\n")
            except KeyError, msg:
                pass
                #sys.stderr.write("ERRO: ThreadTCPcli: KeyError = " + str(msg) + "\n")
            except socket.timeout:
                pass
            except socket.error:
                self.goOnEvent.clear()
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
                cliente.flagTCP.clear()
                try:
                    cliente.send("Silencioso\n")
                    cliente.connfd.shutdown(socket.SHUT_RDWR)
                    cliente.connfd.close()
                except socket.error, msg:
                    sys.stderr.write("ERRO-  %s: Nao foi possivel fechar o socket\n")
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
