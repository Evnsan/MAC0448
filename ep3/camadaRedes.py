#!/usr/bin/python
from datagrama import Datagrama

class CamadaRedes(object):
	def __init__(self):
		self.nomeCamada = 'Redes'	
		super(CamadaRedes, self).__init__()


	## recebe mensagens do transporte e envia para o enlace


	def empacotaDatagrama(self,segmento):
		datag = Datagrama()
		datag.setSegmento(segmento)
		return datag


	def desempacotaDatagrama(self,datagrama):
	   	return datagrama.getSegmento() 