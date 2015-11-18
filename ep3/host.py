#!/usr/bin/env python
from camadaTransporte import CamadaTransporte
from camadaAplicacao import CamadaAplicacao
from camadaRedes import CamadaRedes
from mensagem import Mensagem
from segmento import Segmento
from datagrama import Datagrama

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
        self.comandos = []

        #### funcoes das camadas
        self.cmdaRedes = CamadaRedes()
        self.cmdaTransporte = CamadaTransporte()
        self.cmdaAplicacao = CamadaAplicacao()

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
    
    def setSniffer(self, sniffer):
        self.sniffer = sniffer

    def setPapel(self, papel):
        self.papel = papel
    
    def getHostName(self):
        return self.hostName

    def passo(self, relogio):
        print "HOST(" + self.hostName + "): meu turno"
        try:    
            while relogio >= self.comandos[0][0]:
                #PRECISA ARRUMAR AQUI <================
                print str(self.comandos[0])
                del self.comandos[0]
                self.printComandos()
        except IndexError, msg:
            pass

    def enviar(self):
        msgteste = "teste"
        mensagem = self.cmdaAplicacao.empacotaMensagem(msgteste)
        segmento = self.cmdaTransporte.empacotaSegmento(mensagem)
        datagrama = self.cmdaRedes.empacotaDatagrama(segmento)
        return datagrama

    def receber(self, datagrama):
        segmento = self.cmdaRedes.desempacotaDatagrama(datagrama)
        mensagem = self.cmdaTransporte.desempacotaSegmento(segmento)
        msg = self.cmdaAplicacao.desempacotaMensagem(mensagem)
        return msg

    def recebe(self, datagrama):
        if self.sniffer:
            self.gravaPacote(datagrama)
        self.buff.append(datagrama)
    
    def adicionaComando(self, hora, comando, args):
        self.comandos.append([int(hora), comando, args])
        self.comandos.sort(key = lambda comando: comando[0])

    def printComandos(self):
        print self.comandos

    def gravaPacote(self, datagrama):
        print datagrama
        #gravar no arquivo <================

