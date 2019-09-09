from pantheonModules.exporter.overrides import *
from pantheonModules.pantheonUtilities import events

class DataBase(object):
	
	
	# __widget = None

	def __init__(self,parent = None):
		self._widget = None
		self.__dataName = ""
		self.OnDataUpdate = events.EventHook()

	def _getValue(self):
		return None

	def _setValue(self,*argv):
		pass

	def setName(self,name):
		self.__dataName = name

	def getName(self):
		return self.__dataName

	def setValue(self,*argv):
		self._setValue(*argv)
		self.OnDataUpdate(self)

	def getValue(self):
		return self._getValue()

	def drawElement(self):
		return self._widget