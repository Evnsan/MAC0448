#!/usr/bin/python

from segmento import Segmento

class Datagrama(object):
	def __init__(self):
		self.segmento = None
		super(Datagrama, self).__init__()

	def setSegmento(self,segmento):
		self.segmento = segmento
	def getSegmento(self):
		return self.segmento

	
	