#!/usr/bin/python
from porta import Porta
from camadaRedes import CamadaRedes
class Router(object):
    def __init__(self, nome, numDeInterfaces):
        self.modoVerboso = True
        self.nome = nome
        self.numDeInterfaces = numDeInterfaces
        self.enlaces = []
        self.ips = []
        self.tempoPacote = None
        self.portas = []
        self.sniffer = None
        self.rotas = {} 
        self.passosRestantes = 0
        self.cmdaRedes = CamadaRedes()
        super(Router, self).__init__()
        for i in range(numDeInterfaces):
            porta = Porta()
            self.portas.append(porta)
        ##    self.enlaces.append(None)
        ##    self.ips.append(None)
        ##    self.portas.append(None)


    def __repr__(self):
        return "ROUTER: " + str(self.nome) + " IPS(" + str(self.ips) + ")"

    def setRota(self, remetente, destinatario):
        self.rotas[remetente] = destinatario

    def getRota(self, remetente):
        return rotas[remetente]

    def setEnlace(self, numporta, enlace):
        self.portas[numporta].setEnlace(enlace)
    
    def ipEstaNaRede(self,ipRecebido):
        ipRecebidoSplit = ipRecebido.split('.')
        ipRecebidoSplit[3] = '0'
        ip = ipRecebidoSplit
        destino = self.rotas[ip[0]+'.'+ip[1]+'.'+ip[2]+'.'+ip[3]]
        return destino
    def descobreDestino(self,ipRecebido):
        destino = self.ipEstaNaRede(ipRecebido)
        tamanhoDestino = len(destino.split('.'))
        while tamanhoDestino > 1:
            destino = self.ipEstaNaRede(destino)
            tamanhoDestino = len(destino.split('.'))
        print "ROUTER::DESCOBREDESTINO: achou destino = " + str(destino)
        return destino
    def setPortas(self,args):
        for i in xrange(0,2*int(self.numDeInterfaces),2):
            self.portas[int(args[i])].setTamanhoBuffer(args[i+1]) 

    def setTempoPacote(self,tempo):
        self.tempoPacote = tempo
    
    def passo(self, relogio):
        if self.passosRestantes == 0:
            pass
            #processarPacote:
                #olhar destino
                #decrementar ttl
                #enviar para porta correspondente
            for porta in self.portas:
                if not porta.bufferEstaVazio():
                    datagrama = porta.getDoBuffer()
                    print "ROUTER:" + str(datagrama)
                    destino = int(self.descobreDestino(datagrama.enderecoIpDestino))
                    self.portas[destino].enviar(self, datagrama)
        else:    
            passosRestantes -= 1


        if self.modoVerboso:
            print "ROUTER(" + self.nome + "): Meu turno"
            self.printBuffer()


    def setSniffer(self, numporta, sniffer):
        enlace = self.portas[numporta].getEnlace()
        enlace.setSniffer(sniffer)
    
    def setIp(self, args):
        for i in xrange(0,2*int(self.numDeInterfaces),2):
            self.portas[int(args[i])].setIp(args[i+1]) 
        
##getters e setters

	def getNome(self):
		return self.nomeDoRouter

    def	getPorta(self, numPorta):
        return self.portas[numPorta]

    def printBuffer(self):
        for i in range(len(self.portas)):
            print "ROUTER buffer porta: " + str(i)
            self.portas[i].printBuffer()
