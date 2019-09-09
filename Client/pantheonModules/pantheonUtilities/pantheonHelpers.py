import sys
import os

#LOO FOR WEIRD REIMPORTS
def getPlatformName():
	executable = os.path.basename(sys.executable)

	if "3dsmax" in executable:
		from pymxs import runtime as rt
		release = int(rt.getFileVersion("$max/3dsmax.exe").split("\t")[-1].split(",")[0]) - 3
		if release == 17:
			return MAX_2018_NAME()
		elif release == 16:
			return MAX_2017_NAME()
		else:
			return INVALID()
	elif "mayapy" in executable or "maya" in executable:
		return MAYA_NAME()
	elif "blender" in executable:
		import bpy
		if (2,80,0) < bpy.app.version:
			return BLENDER_280()
		else:
			return BLENDER_279()
	else:
		return NATIVE()


def MAYA_NAME():
	return "MAYA"

def MAX_2017_NAME():
	return "MAX17"

def MAX_2018_NAME():
	return "MAX18"

def BLENDER_279():
	return "BLENDER 2.79"

def BLENDER_280():
	return "BLENDER 2.80"

def NATIVE():
	return "NATIVE"

def INVALID():
	return "INVALID"