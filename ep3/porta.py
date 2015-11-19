#!/usr/bin/python
from datagrama import Datagrama

class Porta(object):
    def __init__(self):
        #definicao dos campos de um segmento
        self.enlace = None
        self.ip = None
        self.tamanhoBuffer = None
        self.buffer = []
        self.modoVerboso = True

        super(Porta, self).__init__()


    def setEnlace(self,enlace):
        self.enlace = enlace

    def getEnlace(self):
        return self.enlace

    
    def setIp(self,ip):
        self.ip = ip

    def getIp(self):
        return self.ip

    def setTamanhoBuffer(self,tamanhoBuffer):
        self.tamanhoBuffer = tamanhoBuffer 

    def getIp(self):
        return self.tamanhoBuffer

    def addNoBuffer(self,pacote):
        #precis fazer
        self.buffer.append(pacote) 

    def bufferEstaVazio(self):
        try:
            if self.buffer[0]:
                return False
        except IndexError:
            return True

    def getDoBuffer(self):
        if self.buffer[0]:
            topoBuffer = self.buffer[0]
            del self.buffer[0]
            return topoBuffer

    def printBuffer(self):
        print self.buffer
        print str(self)
#        for d in self.buffer:
#           print d

    def receber(self, datagrama):
        print "PORTA: vai receber " + str(self)
        self.buffer.append(datagrama)
        print self.buffer

    def enviar(self, router, datagrama):
        if self.modoVerboso:
            print str(self) + ": " + str(datagrama)
        self.enlace.enviar(self, datagrama)
       
    
   

    
   