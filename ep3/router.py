#!/usr/bin/python

import re

from porta import Porta
from camadaRedes import CamadaRedes
class Router(object):
    def __init__(self, nome, numDeInterfaces):
        self.modoVerboso = False 
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
        self.datagramaProcessando = None
        self.portaAtual = numDeInterfaces - 1
        super(Router, self).__init__()
        for i in range(numDeInterfaces):
            porta = Porta()
            self.portas.append(porta)
        ##    self.enlaces.append(None)
        ##    self.ips.append(None)
        ##    self.portas.append(None)


    def __repr__(self):
        return "ROUTER: " + str(self.nome) + " IPS(" + str(self.ips) + ")"
    
    def printBuffer(self):
        for i in range(self.numDeInterfaces):
            print "ROUTER buffer porta: " + str(i)
            self.portas[i].printBuffer()

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
        if self.modoVerboso:
            print "ROUTER::DESCOBREDESTINO: achou destino = " + str(destino)
        return destino
   
    def setPortas(self,args):
        for i in xrange(0,2*int(self.numDeInterfaces),2):
            self.portas[int(args[i])].setTamanhoBuffer(args[i+1]) 

    def setTempoPacote(self,tempo):
        self.tempoPacote = int(self.mysplit(tempo))

    
    def passo(self, relogio):
        if self.modoVerboso:
            print "ROUTER " + str(self.datagramaProcessando)
            print "ROUTER " + str(self.passosRestantes)

        if (self.datagramaProcessando and
            self.passosRestantes == 0):
            
            datagrama = self.datagramaProcessando
            if datagrama.getTTL() > 0:
                datagrama.decrementaTTL()
                ip = datagrama.enderecoIpDestino
                destino = int(self.descobreDestino(ip))
                self.portas[destino].enviar(self, datagrama)
            self.datagramaProcessando = None

        elif not self.datagramaProcessando:
            self.portaAtual = self.proximaPorta()
            if not self.portas[self.portaAtual].bufferEstaVazio():
                if self.modoVerboso:
                    self.printBuffer()
                datagrama = self.portas[self.portaAtual].getDoBuffer()
                self.datagramaProcessando = datagrama
                self.passosRestantes = self.tempoPacote
        else:
            self.passosRestantes -= 1


        if self.modoVerboso:
            print "ROUTER(" + self.nome + "): Meu turno"
            self.printBuffer()


    def setSniffer(self, numporta, sniffer):
        enlace = self.portas[numporta].getEnlace()
        enlace.setSniffer(sniffer)
    
    def setIp(self, args):
        for i in xrange(0,2*int(self.numDeInterfaces),2):
            self.portas[int(args[i])].setIp(args[i+1]) 
       
    def proximaPorta(self):
        teste = self.portaAtual + 1;
        teste %= self.numDeInterfaces
        while (teste != self.portaAtual and
              self.portas[teste].bufferEstaVazio()):
           teste += 1
           teste %= self.numDeInterfaces
        return teste
       
    def mysplit(self, s):
        r = re.compile("([0-9]+)")
        head = r.match(s)
        return head.group(1)

##getters e setters

	def getNome(self):
		return self.nomeDoRouter

    def	getPorta(self, numPorta):
        return self.portas[numPorta]
