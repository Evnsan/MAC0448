#!/usr/bin/python


class Segmento(object):
	def __init__(self):
		#definicao dos campos de um segmento
		self.tamanho = None
		self.mensagem = None
		super(Segmento, self).__init__()
	
	def getTamanho(self):
		return self.tamanho

	def setTamanho(self,tamanho):
		self.tamanho = tamanho

	def setMensagem(self,mensagem):
		self.mensagem = mensagem
	def getMensagem(self):
		return self.mensagem