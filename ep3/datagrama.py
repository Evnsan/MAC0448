#!/usr/bin/python

from segmento import Segmento

# Codigo fonte da Classe Datagrama
#
#

class Datagrama(object):
    def __init__(self, numProtocolo, ipFonte, ipDestino, segmento):
        #cabecalho
        
        self.versao = 4 #4 bits 
        self.IHL = 5 #4 bits
#       self.DSCP = None #6 bits
#       self.ECN = None #2 bits

        self.ComprimentoTotal = None #16 bits
        
        self.identificacao = None #16 bits
        
        #flags  #3 bits
        self.flagsBit0 = False
        #nao vai fragmentar nunca
        self.flagsBit1 = True
        #nao tera outros fragmentos nunca
        self.flagsBit2 = False
        #toda mensagem cabe em um pacote
        self.offset = 0 #13 bits
        
        self.TTL = 64 #8 bits
        self.protocolo = numProtocolo #8 bits

        self.checksum = None #16 bits
        self.enderecoIpFonte = ipFonte #32 bits
        self.enderecoIpDestino = ipDestino #32 bits

        #corpo  
        self.segmento = segmento 
        super(Datagrama, self).__init__()


    def __str__(self):
        return "<PROTO TRANSP>" + str(self.segmento) + "</PROTO TRANSP>"

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

    def calculaChecksum(self):
        #que trampo! <====== remover isso
        #somar inteiros de 16 bits
        #fazer complemento de 1
        #self.checksum = resultado
        pass
