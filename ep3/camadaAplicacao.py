#!/usr/bin/python
from mensagem import Mensagem


class CamadaAplicacao(object):
	def __init__(self, camadaTransporte):
		self.nomeCamada = 'Transporte'	
		super(CamadaAplicacao, self).__init__()
		self.portas = {} #data porta retorna aplicacao
		self.aplicacao= {} #dado nome da aplicacao retorna a aplicacao
		self.clienteDns = None
		self.camadaTransporte = camadaTransporte
        self.buffer = []


	## recebe objetos da aplicacao e devolvem objetos da camada de transporte

	#protocolosAplicacao = {'dns': processaDNS, 'irc': processaIRC}


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

    rotinas = {'ircc': rotinaIrcc,
                'ircs': rotinaIrcs,
                'dnss': rotinaDnss,
                'dnsc': rotinaDnsc,
                }


	def getNoBuffer(self):
		topoBuffer = self.buffer[0]
		del self.buffer[0]
		return topoBuffer

	def adicionaNoBuffer(self, msg):
		self.buffer.append(msg)

	def setAplicacao(self,aplicacao):

		rotinas[aplicacao]()	
		self.aplicacao = aplicacao

	def empacotaMensagem(self,msg,nomeAplicacao):

		m = Mensagem()
		try:
			if self.buffer[0]:
			infoConeccao, comando = rotinas[nomeAplicacao](msg  )
			return "-1"
		except IndexError:
			#if infoConeccao nao eh ip chama DNS, coloca no buffer as msgs do IRC e envia a msg do DNS
			# quando voltar a msg do DNS será enviado a msg do irc do buffer
			infoConeccao, comando = rotinas[nomeAplicacao](msg )
 			adicionaNoBuffer(comando, infoConeccao)
 			m.setMsg(msg)
 			return infoConeccao, m


	def desempacotaMensagem(self,mensagem,porta):
		aplicacao = portas[porta]
		respostaCorreta = aplicacao.recebeMensagem(mensagem)
		if respostaCorreta:
		   m = Mensagem()
		   m.setMsg(getNoBuffer())
		   return m