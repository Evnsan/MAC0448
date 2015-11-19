#!/usr/bin/python

class cabecalhoUdp(object):
    def __init__(self, origem, destino):
        #definicao dos campos de um segmento
        self.ipPortaOrigem = origem
        self.ipPortaDestino = destino
        self.checksum = None
        super(Segmento, self).__init__()

    def __str__(self):
        return ("<UDP-HEAD>" + str(self.portaOrigem) + " " +
                str(self.portaOrigem) + "<UDP-HEAD>")
	
    def setPortaOrigem(self, ip):
	    self.ipPortaOrigem = ip
    
    def getPortaOrigem(self):
	    return self.ipPortaOrigem

    def setPortaDestino(self, ip):
	    self.ipPortaDestino = ip
    
    def getPortaDestino(self):
	    return self.ipPortaDestino

    def setChecksum(self, valor):
        self.checksum = valor
