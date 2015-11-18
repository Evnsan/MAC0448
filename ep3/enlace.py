#!/usr/bin/env python

class Enlace(object):
    def __init__(self, pontaA, pontaB, capacidade, atraso):
        super(Enlace, self).__init__()
        self.portaA = pontaA
        self.portaB = pontaB
        self.buffA = []
        self.buffB = []
        self.sniffer = None
        self.capacidade = capacidade
        self.atraso = atraso

    def passo(self):
        print ("ENLACE(" + str(self.portaA) +
                " <-> " + str(self.portaB) +  "): Meu turno")

    def sefSniffer(self, sniffer):
        self.sniffer = sniffer
