import sys
import json
import glob
sys.path.append('C:/Proyectos/BuildSystem')
from pantheonModules.parser import jsonStructures
from pantheonModules.versioning import requests

exportTypes = ('/**/*.metadata')

basePath = "C:\\Proyectos\\Artmasters\\Animations\\"

files = glob.glob(basePath+exportTypes,recursive=True)
parser = jsonStructures.MayaParser()

counter = {}
counter[-1] = 0;
counter[0] = 0;
counter[1] = 0;
counter[2] = 0;
counter[10] = 0;

for file in files:
	with open(file) as data_file:    
	    data = json.load(data_file)	  
	    ver = parser.getVersion(data)
	    counter[ver] = counter[ver] + 1
	    if ver != -1:
	    	print ( "+++++ " + file +" IS VALID FOR VERSION "+ str(ver) )
	    else:
	    	print ( "----- " + file +" IS INVALID ")

for i in counter:
	print(str(counter[i]) + " number of versions " + str(i))
