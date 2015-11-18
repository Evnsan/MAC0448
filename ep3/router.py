#!/usr/bin/python

class Router(object):
    def __init__(self, nome, numDeInterfaces):
        self.nome = nome
        self.numDeInterfaces = numDeInterfaces
        self.enlaces = []
        self.tempoPacote = None
        self.portas = {}
        self.sniffer = None
        super(Router, self).__init__()

    def setEnlace(se,fposEnlace, enlace):
        self.enlaces[posEnlace] = enlace

    def setPortas(self,args):
        for i in xrange(0,2*int(self.numDeInterfaces),2):
            self.portas[args[i]] = args[i+1] 
		
    def setTempoPacote(self,tempo):
        self.tempoPacote = tempo
    
    def passo(self, relogio):
        print "ROUTER(" + self.nome + "): Meu turno"

    def setSniffer(self, porta, sniffer):
        enlace = enlaces[porta]
        enlace.setSniffer(sniffer)
##getters e setters

	def getNome(self):
		return self.nomeDoRouter
	
