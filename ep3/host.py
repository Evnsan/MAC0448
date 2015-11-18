#!/usr/bin/env python

# Arquivo com o codigo da classe Host do simulador de rede
#

class Host(object):
    def __init__(self, hostName):
        super(Host, self).__init__()
        self.hostName = hostName
        self.ip = ''
        self.ipRoteador = ''
        self.ipDnsServidor = ''
        self.sniffer = None
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
        self.sniffer = sniffer

    def setPapel(self, papel):
        self.papel = papel
    
    def getHostName(self):
        return self.hostName

    def passo(self):
        print "HOST(" + self.hostName + "): meu turno"
