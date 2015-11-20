#!/usr/bin/python
from mensagem import Mensagem


class CamadaAplicacao(object):
	def __init__(self):
		self.nomeCamada = 'Transporte'	
		super(CamadaAplicacao, self).__init__()
		self.portas = {} #data porta retorna aplicacao
		self.aplicacao= {} #dado nome da aplicacao retorna a aplicacao
		self.camadaTransporte = None
        


	## recebe objetos da aplicacao e devolvem objetos da camada de transporte

	#protocolosAplicacao = {'dns': processaDNS, 'irc': processaIRC}
	def passo3(self):
		for app in self.aplicacao:
			app.passo3()
	def setCamadaTransporte(self, camadaTransporte):
		self.camadaTransporte = camadaTransporte


   

	def rotinaIrcc(self):
		ircc = Ircc(self.camadaTransporte, '6688')
		aplicacao['ircc'] = ircc
		portas['6688'] = ircc 

	def rotinaIrcs(self):
		print "RotinaIRcs"

	def rotinaDnss(self):
		print "RotinaDnss"

	def rotinaDnsc(self):
		print "RotinaDnsc"

	def getNoBuffer(self):
		topoBuffer = self.buffer[0]
		del self.buffer[0]
		return topoBuffer

	def adicionaNoBuffer(self, msg):
		self.buffer.append(msg)

	def setAplicacao(self,aplicacao):
		if aplicacao == 'ircc':
			rotinaIrcc()	
		if aplicacao == 'ircs':
			rotinaIrcs()
		if aplicacao == 'dnss':
			rotinaDnss()	
		if aplicacao == 'dnsc':
			rotinaDnsc()	
		self.aplicacao = aplicacao

	

	def desempacotaMensagem(self,mensagem,porta):
		aplicacao = portas[porta]
		respostaCorreta = aplicacao.recebeMensagem(mensagem)
		if respostaCorreta:
		   m = Mensagem()
		   m.setMsg(getNoBuffer())
		   return m