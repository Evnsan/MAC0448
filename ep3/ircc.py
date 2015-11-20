#!/usr/bin/python

from mensagem import Mensagem
class Ircc(object):
    def __init__(self, camadaTransporte, portaOrigem):
        self.servidorIp = None
        self.servidorPorta = None
        self.nomeUsuario = None
        self.estado = None
        self.bloqueado = False
        self.buffer = []
        self.camadaTransporte = camadaTransporte
        self.portaOrigem = portaOrigem
        super(Ircc, self).__init__()


    def passo3(self):
        while len(self.buffer) > 0 and not self.bloqueado:
            args = self.buffer[0]
            del self.buffer[0]
            cmd = args[0]
            del args[0]
            if 'CONNECT' == cmd:
                self.cmdConnect(args[0])
            if 'USER' == cmd:
                self.cmdUser(args[0])
            if 'QUIT' == cmd:
                self.cmdQuit(args[0])
           


    estado = {'CONECTADO' ,'NAOCONECTADO', 'LOGADO'}
    def novoComando(self,comando):
        self.buffer.append(comando)
    
    def cmdConnect(self,args):
        temp = args[0].split(".")
        if len(temp) > 1: 
            self.servidorIp = args[0]
        else:
            #fazer chamada DNS
            self.bloqueado = True
        self.servidorPorta = args[1]
       

    def cmdUser(self, args):
        m = Mensagem()
        m.setMsg("USER " + str(args[0]) + " 8 *")
        self.envia(m)
    
    def cmdQuit(self, args):
        m = Mensagem()
        m.setMsg(args[0])
        self.envia(m)

    def envia(self,m):
        self.camadaTransporte.enviaMensagem(m,'UDP',self.portaOrigem, self.servidorPorta, self.servidorIp)


   

    def realizaRotina(self, comando):
        comando = comandos[0]
        del comandos[0]
        retorno = comandos[comando](comandos[0])
        return retorno  

   
