#!/usr/bin/python

class Router(object):
    def __init__(self, nome, numDeInterfaces):
        self.nome = nome
        self.numDeInterfaces = numDeInterfaces
        self.enlaces = []
        self.ips = []
        self.tempoPacote = None
        self.portas = {}
        self.sniffer = None
        self.rotas = {} 
        super(Router, self).__init__()
        for i in range(numDeInterfaces):
            self.enlaces.append(None)
            self.ips.append(None)

    def __repr__(self):
        return "ROUTER: " + str(self.nome) + " IPS(" + str(self.

    def setRota(self, remetente, destinatario):
        self.rotas[remetente] = destinatario

    def getRota(self, remetente):
        return rotas[remetente]

    def setEnlace(self, porta, enlace):
        self.enlaces[porta] = enlace

    def setPortas(self,args):
        for i in xrange(0,2*int(self.numDeInterfaces),2):
            self.portas[args[i]] = args[i+1] 
		
    def setTempoPacote(self,tempo):
        self.tempoPacote = tempo
    
    def passo(self, relogio):
        print "ROUTER(" + self.nome + "): Meu turno"

    def setSniffer(self, porta, sniffer):
        enlace = self.enlaces[porta]
        enlace.setSniffer(sniffer)
    
    def setIp(self, args):
        pass
        
##getters e setters

	def getNome(self):
		return self.nomeDoRouter
	
