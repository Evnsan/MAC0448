#!/usr/bin/python

class Parser(object):
    def __init__(self):
        self.nomeArqConfiguracao = "modeloConfig"
        super(Parser, self).__init__()
    
    def setArqConfiguracao(self, nome):
        self.nomeArqConfiguracao = nome

    def leituraDaConfiguracao(self):
	    with open(self.nomeArqConfiguracao) as f:
             conteudo = f.readlines()
             return conteudo
    
    def filtraComentarios(self, conteudo):
        saida = []
        for linha in conteudo:
            if(linha[0] != '#'):
                saida.append(linha)
        return saida

    def filtraQuebraLinha(self, conteudo):	
        saida = []
        tmp = []
        buff = ""
        for linha in conteudo:
            tmp.append(linha.split('\n')[0])
        for linha in tmp:
            buff += linha
            if not linha.endswith('\\'):
                saida.append(buff)
                buff = ''
            else:
                buff = buff.split('\\')[0]
        return saida	

    def filtraArg(self, conteudo):
        saida = []
        for comando in conteudo:
            cmd = []
            tmp = comando.split(' ')
            cmd.append(tmp[0])
            del tmp[0]
            cmd.append(tmp)
            saida.append(cmd)
        return saida

    def lerComandos(self):
        self.leituraDaConfiguracao()
        leituraCfg = self.leituraDaConfiguracao()
        leituraSemComentarios = self.filtraComentarios(leituraCfg)
        leituraSemQuebraLinha = self.filtraQuebraLinha(leituraSemComentarios)
        leituraComArgumentosFormatados = self.filtraArg(leituraSemQuebraLinha)
        return leituraComArgumentosFormatados
