from pantheonModules.conn.requests import ServerRequest
from pantheonModules.conn import serverObjects

currentProject = ""
serverProjects = None



def loadProjects():
	global currentProject
	global serverProjects

	serverProjects = ServerRequest.mongoList(serverObjects.GameProjects)
	print(serverProjects)
	currentProject = serverProjects.objects[0].name

def changeProject(pName):
	print("CHANGING!")
	global currentProject
	global serverProjects

	if pName in [proj.name for proj in serverProjects.objects]:
		currentProject = pName
	else:
		print("This projects does not exist in the list")

def getCurrentProject():
	global currentProject
	return currentProject


loadProjects()