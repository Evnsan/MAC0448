#!/usr/bin/python


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
            self.comandos[cmd](args)


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
        self.envia(m)

    def cmdUser(self, args):
        m = Mensagem()
        m.setMsg(args+ " 8 *")
        self.envia(m)
    
    def cmdQuit(self, args):
        m = Mensagem()
        m.setMsg(args)
        self.envia(m)

    def envia(self,m):
        self.camadaTransporte.enviaMensagem(m,'UDP',self.portaOrigem, self.servidorPorta)


    comandos = {'CONNECT': cmdConnect,
                'USER': cmdUser,
                'QUIT': cmdQuit}

    def realizaRotina(self, comando):
        comando = comandos[0]
        del comandos[0]
        retorno = comandos[comando](comandos[0])
        return retorno  

   
