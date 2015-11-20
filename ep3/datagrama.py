#!/usr/bin/python

from segmento import Segmento

# Codigo fonte da Classe Datagrama
# o datagrama para uma comunicacao sobre IP
# basicamente o cabecalho IP + segmento

class Datagrama(object):
    def __init__(self, numProtocolo, ipFonte, ipDestino, segmento):
        
        #cabecalho

        self.comprimentoTotal = segmento.getTamanho() + 14 #16 bits
        self.TTL = 64 #8 bits
        self.protocolo = numProtocolo #8 bits
        self.enderecoIpFonte = ipFonte #32 bits
        self.enderecoIpDestino = ipDestino #32 bits
        
        #corpo  
        self.segmento = segmento 
        super(Datagrama, self).__init__()

    def __str__(self):
        return ("CAMADA DE REDE:\n"
                + "Endereco IP de origem: " + str(self.enderecoIpFonte) + "\n"
                + "Endereco IP de destino: " + str(self.enderecoIpDestino)+"\n"
                + "Protocolo: " + str(self.protocolo) + "\n"
                + "Tamanho total: " + str(self.comprimentoTotal) + "\n"
                + "TTL: " + str(self.TTL) + "\n"
                + str(self.segmento) )

    def setSegmento(self,segmento):
        self.segmento = segmento
    def getSegmento(self):
        return self.segmento
    def getTamanho(self):
        return self.comprimentoTotal

    def setTamanho(self, tam):
        self.comprimentoTotal = tam
	
    def setProtocolo(self, numProtocolo):
        # numProtocolo TCP = 6    
        # numProtocolo UDP = 17
        self.protocolo = numProtocolo

    def decrementaTTL(self):
        self.TTL -= 1

    def getTTL(self):
        return self.TTL
