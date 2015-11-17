#!/usr/bin/env python

class Host(object):
    def __init__(self, hostName):
        super(Host, self).__init__()
        self.hostName = hostName
        self.ip = ''
        self.ipRoteador = ''
        self.ipDnsServidor = ''
        self.snifferFile = None
        self.enlace = None
        self.buff = []
        self.papel = ''

    def setIp(self, args):
        if not isinstance(args, basestring):
    
            try:
                self.ipDnsServidor = args[2]
                self.ipRoteador = args[1]
                self.ip = args[0]
            except IndexError, msg:
                print ("HOST(SETIP) - Hostname = " + self.hostName 
                       + ": Argumentos Insuficientes.")
                print "    " + str(msg)
        else:
            print ("HOST(" + self.hostName + ").setIp()"
                   + ": Argumentos devem ser listas")
            print "HOST(" + self.hostName + ") Recebido:" + str(args)

    def setEnlace(self, enlace):
        self.enlace = enlace
    
    def sefSniffer(self, sniffer):
        self.snifferFile = sniffer

    def setPapel(self, papel):
        self.papel = papel

