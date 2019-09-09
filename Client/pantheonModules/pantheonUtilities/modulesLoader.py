import inspect
import os
import sys
import importlib

class ModulesLoader():
	
	modulesName = "pantheonModules"
	modulesPath = ""

	def __init__(self):
		rootPath = inspect.getfile(inspect.currentframe()) 

		failSafeCounter = 25
		while os.path.basename(rootPath) != self.modulesName  and failSafeCounter > 0 :
			failSafeCounter = failSafeCounter - 1
			rootPath = os.path.dirname(rootPath)
			
		self.modulesPath = rootPath

	def __call__(self, name):
		if self.modulesPath not in sys.path:
			sys.path.append(self.modulesPath)
		if name not in sys.modules:
			return importlib.import_module(name)
		else:
			module = sys.modules[name]
			return reload(module)