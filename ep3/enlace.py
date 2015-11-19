#!/usr/bin/env python
import re
import math
from collections import deque

class Enlace(object):
    def __init__(self, portaA, portaB, capacidade, atraso):
        super(Enlace, self).__init__()

        self.modoVerboso = False 
        
        #pontaA
        self.portaA = portaA
        self.buffA = deque() 
        self.temposA = deque() 

        #pontaB
        self.portaB = portaB
        self.buffB = deque() 
        self.temposB = deque()
        
        #dados internos
        self.sniffer = None
        self.capacidade = self.mysplit(capacidade)
        self.atraso = self.mysplit(atraso)

    def __repr__(self):
        return ("ENLACE: [" + str(self.portaA) + 
                    " --> " + str(self.portaB) + "]")
    
    def __str__(self):
        return ("ENLACE: [" + str(self.portaA) + 
                    " --> " + str(self.portaB) + "]")

    def passo(self, relogio):
        if self.modoVerboso:
            print ("ENLACE(" + str(self.portaA) +
                   " <-> " + str(self.portaB) +  "): Meu turno")
        self.processa(self.temposA, self.buffA, self.portaA, relogio)
        self.processa(self.temposB, self.buffB, self.portaB, relogio)
   
    def processa(self, tempos, buff, porta, relogio):
        if len(tempos) > 0:
            if tempos[0] == 0 :
                porta.recebe(buff[0])
                if self.sniffer:
                    self.gravaDatagrama(buff[0], relogio)
                tempos.popleft()
                buff.popleft()
            else:
                tempos[0] -= 1;
        elif self.modoVerboso:
               print "ENLACE::PROCESSA : Nada para processar"
        if self.modoVerboso:
           print str(self) 
           self.printBuff()

    def gravaDatagrama(self, datagrama, relogio):
        msg = "[" + str(relogio) + "]: " + str(datagrama)
        with open(self.sniffer, 'a') as arquivo:
            arquivo.write(msg + '\n')
        print "SNIFFER " + msg
        #gravar no arquivo <===================

    def setSniffer(self, sniffer):
        self.sniffer = sniffer

    def mysplit(self, s):
        r = re.compile("([0-9]+)")
        head = r.match(s)
        return head.group(1)

    def enviar(self, remetente, datagrama):
        tempo = math.ceil(float(datagrama.getTamanho()) /
                float(self.capacidade) + float(self.atraso))
        if(remetente == self.portaA):
            self.buffA.append(datagrama)
            self.temposA.append(tempo)
        elif(remetente == self.portaB):
            self.buffB.append(datagrama)
            self.temposB.append(tempo)

    def printBuff(self):
        print "ENLACE::PRINTBUFF:______________"
        print "portaA"
        print self.temposA
        print self.buffA
        print "portaB"
        print self.temposB
        print self.buffB
        print "________________________________"


    def setTerminalA(self, terminal):
       self.portaA = terminal 
    
    def setTerminalB(self, terminal):
       self.portaB = terminal 
