from .exportable import *

class exportablePackage(exportable): #DEPRECATED

	packageType = None
	packageSubType = None

	objectsToExport = [] #exportableContent

	def __init__(self,objects):
		self.objectsToExport = objects