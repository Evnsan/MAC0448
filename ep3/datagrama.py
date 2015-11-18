#!/usr/bin/python

class Datagrama(object):
    def __init__(self):
        self.tamanho = None
        super(Datagrama, self).__init__()

    def getTamanho(self):
        return self.tamanho

    def setTamanho(self, tam):
        self.tamanho = tam
