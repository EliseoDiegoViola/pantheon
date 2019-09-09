from pantheonModules.conn.requests import ServerRequest


serverLoaded = False

def init():
	if not serverLoaded:
		serverLoaded = loadServerData()



	