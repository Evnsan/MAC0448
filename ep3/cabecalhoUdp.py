#!/usr/bin/python

class CabecalhoUdp(object):
    def __init__(self, origem, destino):
        #definicao dos campos de um segmento
        self.ipPortaOrigem = origem
        self.ipPortaDestino = destino
        self.tamanho = 4 # no inicio so cabecalho # 2 portas de 16 bits 
        super(CabecalhoUdp, self).__init__()

    def __str__(self):
        return ("(UDP):\n" 
                + "Porta fonte: " + str(self.ipPortaOrigem) + "\n"
                + "Porta destino: " + str(self.ipPortaDestino) + "\n"
                + "Tamanho do cabecalho UDP + mensagem: " + str(self.tamanho) )
	
    def setPortaOrigem(self, ip):
	    self.ipPortaOrigem = ip
    
    def getPortaOrigem(self):
	    return self.ipPortaOrigem

    def setPortaDestino(self, ip):
	    self.ipPortaDestino = ip
    
    def getPortaDestino(self):
	    return self.ipPortaDestino

    def getTamanho(self):
	    return self.tamanho 
    
    def setTamanho(self, valor):
        self.tamanho = valor + 4
