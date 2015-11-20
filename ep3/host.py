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
    def __init__(self, nome):
        super(Host, self).__init__()
        self.modoVerboso = False 

        self.nome = nome
        self.ip = ''
        self.ipRoteador = ''
        self.ipDnsServidor = ''
        self.sniffer = None
        self.enlace = None
        self.buff = []
        self.papel = ''
        self.comandos = []
        self.nomeAplicacao = None

        #### funcoes das camadas
        self.cmdaRedes = CamadaRedes(self)
        self.cmdaAplicacao = CamadaAplicacao()
        self.cmdaTransporte = CamadaTransporte( self.cmdaRedes, self.cmdaAplicacao)
        self.cmdaRedes.setCamadaTransporte(self.cmdaTransporte)
        self.cmdaAplicacao.setCamadaTransporte(self.cmdaTransporte)

    
    def __str__(self):
        return "HOST: " + str(self.nome) + " IP(" + str(self.ip) + ")"
    
    def __repr__(self):
        return "HOST " + str(self.nome) + " IP=" + str(self.ip)

    
    def setIp(self, args):
        if not isinstance(args, basestring):
            try:
                self.ipDnsServidor = args[2]
                self.ipRoteador = args[1]
                self.ip = args[0]
                self.cmdaRedes.setIp(self.ip)
            except IndexError, msg:
                print ("HOST(SETIP) - Hostname = " + self.nome 
                       + ": Argumentos Insuficientes.")
                print "    " + str(msg)
        else:
            print ("HOST(" + self.nome + ").setIp()"
                   + ": Argumentos devem ser listas")
            print "HOST(" + self.nome + ") Recebido:" + str(args)

    def getEnlace(self):
        return self.enlace

    def setEnlace(self, enlace):
        self.enlace = enlace
        self.cmdaRedes.setEnlace(enlace)
    
    def setSniffer(self, sniffer):
        #self.sniffer = sniffe0r
        self.enlace.setSniffer(sniffer)

    def setPapel(self, papel):
        self.papel = papel
        self.cmdaAplicacao.setAplicacao(papel)
    
    def getHostName(self):
        return self.nome

    
    def bufferEstaVazio(self):
        try:
            if self.buff[0]:
                return False
        except IndexError:
            return True

    def getDoBuffer(self):
        if self.buff[0]:
            topoBuff = self.buff[0]
            del self.buff[0]
            return topoBuff

    def passo(self, relogio):
        if self.modoVerboso:
            print "HOST(" + self.nome + "): meu turno"
        try:    
            while relogio >= self.comandos[0][0]:
                #PRECISA ARRUMAR AQUI <================
                del self.comandos[0][0] #deleta o tempo do comando
                if self.modoVerboso:
                    print ("PASSO::host: comando a ser executado" 
                           + str(self.comandos[0]))
                self.cmdaAplicacao.novoComando(self.papel,self.comandos[0])
                del self.comandos[0]
                if self.modoVerboso:
                    self.printComandos()
        except IndexError, msg:
            pass
        if not self.bufferEstaVazio():
            #datagrama = self.getDoBuffer()
            #segmento = self.cmdaRedes.desempacotaDatagrama(datagrama)
            #mensagem = self.cmdaTransporte.desempacotaSegmento(segmento)
            #msg = self.cmdaAplicacao.desempacotaMensagem(mensagem)
            if self.modoVerboso:
                print "HOST " + str(self.nome) + ": Tem mensagem no buffer"
        self.cmdaAplicacao.passo3()


    

 #   def receber(self, datagrama):
 #       segmento = self.cmdaRedes.desempacotaDatagrama(datagrama)
 #       mensagem = self.cmdaTransporte.desempacotaSegmento(segmento)
 #       msg = self.cmdaAplicacao.desempacotaMensagem(mensagem)
 #       return msg

    def receber(self, datagrama):
        self.buff.append(datagrama)
    
    def adicionaComando(self, hora, comando, args):
        self.comandos.append([int(hora), comando, args])
        self.comandos.sort(key = lambda comando: comando[0])

    def printComandos(self):
        print "HOST::PRINTCOMANDOS: " + str(self.comandos)

