#!/usr/bin/python


from segmento import Segmento

class Datagrama(object):
    def __init__(self):
        self.segmento = None
        self.tamanho = None
        super(Datagrama, self).__init__()


    def __str__(self):
        return "<PROTO TRANSP>" + str(self.segmento) + "</PROTO TRANSP>"

    def setSegmento(self,segmento):
        self.segmento = segmento
    def getSegmento(self):
        return self.segmento
    def getTamanho(self):
        return self.tamanho

    def setTamanho(self, tam):
        self.tamanho = tam
	
	
