#!/usr/bin/python
from mensagem import Mensagem


class CamadaAplicacao(object):
	def __init__(self):
		self.nomeCamada = 'Transporte'	
		super(CamadaAplicacao, self).__init__()


	## recebe objetos da aplicacao e devolvem objetos da camada de transporte

	#protocolosAplicacao = {'dns': processaDNS, 'irc': processaIRC}

	def empacotaMensagem(self,msg):
		m = Mensagem()
		m.setMsg(msg) 
		return m

	def desempacotaMensagem(self,mensagem):
		return mensagem.getMsg()