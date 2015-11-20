#!/usr/bin/python

from cabecalhoUdp import CabecalhoUdp


class Segmento(object):
    def __init__(self, protocolo, origem, destino):
        #definicao dos campos de um segmento
        self.cabecalho = None
        self.mensagem = None
        self.portaOrigem = origem
        self.portaDestino = destino
        super(Segmento, self).__init__()
        if protocolo == 'UDP':
            self.cabecalho = CabecalhoUdp(origem, destino)

    def __str__(self):
        return ("CAMADA DE TRANSPORTE " + str(self.cabecalho) + "\n"
                + str(self.mensagem))
	
    def getTamanho(self):
        return self.cabecalho.getTamanho()

    def setTamanho(self,tamanho):
        self.cabecalho.setTamanho(tamanho)

    def setMensagem(self,mensagem):
        self.mensagem = mensagem
        self.cabecalho.setTamanho(mensagem.getTamanho())

    def getMensagem(self):
        return self.mensagem
