#!/usr/bin/env python

class Enlace(object):
    def __init__(self, pontaA, pontaB):
        super(Enlace, self).__init__()
        self.portaA = PontaA
        self.portaB = PontaB
        self.buffA = []
        self.buffB = []
        self.sniffer = None

    def sefSniffer(self, sniffer):
        self.sniffer = sniffer
