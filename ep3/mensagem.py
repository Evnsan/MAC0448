#!/usr/bin/python


class Mensagem(object):
    def __init__(self):
        #definicao dos campos de um segmento
        self.msg = None
        super(Mensagem, self).__init__()
		
    def __str__(self):
        return "<PROTO MSG>" + str(self.msg) + "</PROTO MSG>"

    def getMsg(self):
        return self.msg

    def setMsg(self,msg):
        self.msg = msg
