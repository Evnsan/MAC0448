#!/usr/bin/python

class Porta(object):
    def __init__(self):
        #definicao dos campos de um segmento
        self.enlace = None
        self.ip = None
        self.tamanhoBuffer = None
        self.buffer = []

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
        self.tamanhoBuffer = tamanhoBuffer 

    def getDoBuffer(self):
        if self.buffer[0]:
            topoBuffer = self.Buffer()
            del self.buffer[0]
            return topoBuffer
       
    
   

    
   