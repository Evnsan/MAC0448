#!/usr/bin/python
from segmento import Segmento

class CamadaTransporte(object):
	def __init__(self, camadaRede, camadaAplicacao):
		self.nomeCamada = 'Transporte'	
		self.camadaRede = camadaRede
		self.camadaAplicacao = camadaAplicacao
		super(CamadaTransporte, self).__init__()


	##entende da camada de redes e processa para a camada de aplicacao 
	##entende objetos da aplicacao e processa para camada de redes

	#protocolosTransporte = {'TCP': processaTCP, 'UDP': processaUDP}

	def empacotaSegmento(self,Mensagem):
		seg = Segmento()
		seg.setMensagem(Mensagem)
		return seg
	def desempacotaSegmento(self,segmento):
		return segmento.getMensagem()

	def enviaMensagem(self,m, protocolo,portaOrigem, portaDestino, ipServidor):
		seg = Segmento(protocolo, portaOrigem, portaDestino)
		seg.setMensagem(m)
		self.camadaRede.enviaSegmento(protocolo, ipServidor, seg)
	