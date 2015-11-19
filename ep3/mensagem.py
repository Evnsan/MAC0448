#!/usr/bin/python


class Mensagem(object):
    def __init__(self):
        #definicao dos campos de um segmento
        self.msg = None
        self.tamanho = 0
        super(Mensagem, self).__init__()
		
    def __str__(self):
        return ("CAMADA DE APLICACAO:" + "\n"
                + str(self.msg) )

    def getMsg(self):
        return self.msg

    def setMsg(self, msg):
        self.msg = msg
        self.tamanho = len(msg) #usando 1 byte por char 

    def getTamanho(self):
        return self.tamanho

