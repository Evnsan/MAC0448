#!/usr/bin/env python
import re
import math
from collections import deque

class Enlace(object):
    def __init__(self, portaA, portaB, capacidade, atraso):
        super(Enlace, self).__init__()
        
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

    def passo(self, relogio):
        print ("ENLACE(" + str(self.portaA) +
                " <-> " + str(self.portaB) +  "): Meu turno")
        print self.capacidade
        print self.atraso
        self.processa(self.temposA, self.buffA, self.portaA)
        self.processa(self.temposB, self.buffB, self.portaB)
   
    def processa(self, tempos, buff, porta):
        if len(tempos) > 0:
            if tempos[0] == 0 :
                porta.recebe(buff[0])
                tempos.popleft()
                buff.popleft()
            else:
                tempos[0] -= 1;
        else:
            print "ENLACE::PROCESSA : Nada para processar"

    def sefSniffer(self, sniffer):
        self.sniffer = sniffer

    def mysplit(self, s):
        r = re.compile("([0-9]+)")
        head = r.match(s)
        return head.group(1)

    def enviar(self, remetente, datagrama):
        tempo = math.ceil(float(datagrama.getTamanho()) /
                float(self.capacidade))
        if(remetente == self.portaA):
            self.buffA.append(datagrama)
            self.temposA.append(tempo)
        elif(remetente == self.portaB):
            self.buffB.append(datagrama)
            self.temposB.append(tempo)

    def printBuff(self):
        print self.temposA
        print self.buffA
        print self.temposB
        print self.buffB
