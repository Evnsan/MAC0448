#!/usr/bin/python
from datagrama import Datagrama

class CamadaRedes(object):
	def __init__(self, hst):
		self.nomeCamada = 'Redes'	
		self.ip = None
		self.enlace = None
		self.hst = hst
		self.camadaTransporte = None
		super(CamadaRedes, self).__init__()


	## recebe mensagens do transporte e envia para o enlace
	def setEnlace(self, enlace):
		self.enlace = enlace

	def setIp(self,ip):
		self.ip = ip

	def setCamadaTransporte(self,camadaTransporte):
		self.camadaTransporte = camadaTransporte

	def empacotaDatagrama(self,segmento):
		datag = Datagrama()
		datag.setSegmento(segmento)
		return datag


	def desempacotaDatagrama(self,datagrama):
	   	return datagrama.getSegmento() 

   	def enviaSegmento(self,protocolo, ipServidor, seg):
   		datagrama = Datagrama(protocolo, self.ip, ipServidor, seg)
   		self.enlace.enviar(self.hst,datagrama)
