#!/usr/bin/env python

class Enlace(object):
    def __init__(self, pontaA, pontaB, capacidade, atraso):
        super(Enlace, self).__init__()
        self.portaA = PontaA
        self.portaB = PontaB
        self.buffA = []
        self.buffB = []
        self.sniffer = None
        self.capacidade = capacidade
        self.atraso = atraso

    def sefSniffer(self, sniffer):
        self.sniffer = sniffer