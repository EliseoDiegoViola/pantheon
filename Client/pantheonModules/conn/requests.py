from .responses import ServerResponse
from pantheonModules.logger.ateneaLogger import AteneaLogger
from . import serverObjects
import json
try:
    import http.client as httpC
except ImportError:
    print("Using Python 2.x URL module")
    import httplib as httpC

    




mainServerUrl = "127.0.0.1"
backUpServerUrl = "127.0.0.1"


class ServerRequest():

	serverUrl = ""
	serverPort = 13370

	@staticmethod
	def tryMainServer():
		if not ServerRequest.serverUrl:
			try:
				conn = httpC.HTTPConnection(host = mainServerUrl, port = ServerRequest.serverPort)
				conn.request(method = 'GET', url = '/')
				response = conn.getresponse()
				print(mainServerUrl, "is working!")
				ServerRequest.serverUrl = mainServerUrl
				return
			except Exception as e:
				print("ERROR IS ", e)

			try:
				conn = httpC.HTTPConnection(host = backUpServerUrl, port = ServerRequest.serverPort)
				conn.request(method = 'GET', url = '/')
				response = conn.getresponse()
				print(backUpServerUrl, "is working!")
				ServerRequest.serverUrl = backUpServerUrl
				return
			except Exception as e:
				print("ERROR IS ", e)
		else:
			print ("Server Found in " + ServerRequest.serverUrl)
	@staticmethod
	def getToolData(dataName):
		ServerRequest.tryMainServer()

		serverUrl = ServerRequest.serverUrl
		serverPort = ServerRequest.serverPort
		serverRes = ServerResponse()
		try:
			# reqUrl = "http://" + serverUrl+":"+str(serverPort)+'/tools/data/'+dataName
			# response = url.urlopen(reqUrl)

			hdr = {"content-type": "application/json"}
			conn = httpC.HTTPConnection(host = serverUrl, port = serverPort)
			conn.request(method = 'GET', url = '/tools/data/'+dataName, body = None, headers = hdr)
			response = conn.getresponse()
			# print "!!!!! LA PUTA " , response.read().decode('utf-8')

			serverRes.header = response.msg 
			serverRes.body = response.read().decode('utf-8')
			serverRes.returnCode = response.status
			serverRes.errorCode = 0
			serverRes.errorMessage = ""
			 
		except Exception as e:
			serverRes.header = hdr
			serverRes.body =""
			serverRes.returnCode = 500
			serverRes.errorCode = 501
			serverRes.errorMessage = AteneaLogger.ErrorHandler.GetErrorMessage(str(serverRes.errorCode),str(e))

			ServerRequest.serverUrl = ""

		return serverRes

	@staticmethod
	def sendToHermes(message):
		ServerRequest.tryMainServer()

		serverUrl = ServerRequest.serverUrl
		serverPort = ServerRequest.serverPort
		serverRes = ServerResponse()

		try:
			hdr = {"content-type": "application/json"}
			values = {}
			values["msg"] = message

			conn = httpC.HTTPConnection(host = serverUrl, port = serverPort)
			conn.request(method = 'POST', url = '/tools/hermes/message', body = json.dumps(values), headers = hdr)
			response = conn.getresponse()

			serverRes.header = response.msg 
			serverRes.body = response.read().decode('utf-8')
			serverRes.returnCode = response.status
			serverRes.errorCode = 0
			serverRes.errorMessage = ""
		except Exception as e:

			serverRes.header = hdr 
			serverRes.body = ""
			serverRes.returnCode = 500
			serverRes.errorCode = 501
			serverRes.errorMessage = AteneaLogger.ErrorHandler.GetErrorMessage(str(serverRes.errorCode),str(e))
				
			ServerRequest.serverUrl = ""

		return serverRes

	@staticmethod
	def mongoList(mongoClass,searchFilter = None):
		ServerRequest.tryMainServer()

		serverUrl = ServerRequest.serverUrl
		serverPort = ServerRequest.serverPort

		serverRes = ServerResponse()
		collection = mongoClass.__name__
		if not searchFilter:
			url = '/'+collection
		else:
			url = '/'+collection+'/filterBy/'+searchFilter["filterName"]+'/'+searchFilter["filterValue"]
		print (url)

		try:
			hdr = {"content-type": "application/json"}
			conn = httpC.HTTPConnection(host = serverUrl, port = serverPort)
			conn.request(method = 'GET', url = url, body = None, headers = hdr)
			response = conn.getresponse()
			#print(response.read().decode('utf-8'))

			serverRes.header = response.msg 
			serverRes.body = json.loads(response.read().decode('utf-8'))
			serverRes.returnCode = response.status
			serverRes.errorCode = 0
			serverRes.errorMessage = ""
			
			objectsList = []
			for obj in serverRes.body:
				# if searchFilter :
				# 	print("BODY IS ", obj)
				objectsList.append(mongoClass.initFromJsonObject(obj))
			serverRes.objects = objectsList

		except Exception as e:
			print("EXCEPTION ", e)
			serverRes.header = hdr 
			serverRes.body = ""
			serverRes.returnCode = 500
			serverRes.errorCode = 501
			serverRes.errorMessage = AteneaLogger.ErrorHandler.GetErrorMessage(str(serverRes.errorCode),[str(e)])
			
			ServerRequest.serverUrl = ""

		return serverRes

	@staticmethod
	def mongoCreate(serverObject):
		ServerRequest.tryMainServer()

		serverUrl = ServerRequest.serverUrl
		serverPort = ServerRequest.serverPort

		if not issubclass(serverObject.__class__ ,serverObjects.MongoObject):
			print( "Error {0} is not a mongo object!".format(serverObject))

		serverRes = ServerResponse()
		collection = serverObject.__class__.__name__
		try:
			hdr = {"content-type": "application/json"}
			conn = httpC.HTTPConnection(host = serverUrl, port = serverPort)
			conn.request(method = 'POST', url = '/'+collection, body = json.dumps(serverObject.toDict()), headers = hdr)
			response = conn.getresponse()

			serverRes.header = response.msg 
			serverRes.body = json.loads(response.read().decode('utf-8'))
			serverRes.returnCode = response.status
			serverRes.errorCode = 0
			serverRes.errorMessage = ""
			objectList = [serverObject]
			serverRes.objects = objectList


			if serverRes.returnCode == 200:
				serverObject.mongoId = serverRes.body["id"]

		except Exception as e:
			serverRes.header = hdr 
			serverRes.body = ""
			serverRes.returnCode = 500
			serverRes.errorCode = 501
			serverRes.errorMessage = AteneaLogger.ErrorHandler.GetErrorMessage(str(serverRes.errorCode),[str(e)])
			
			ServerRequest.serverUrl = ""

		return serverRes

	@staticmethod
	def mongoUpdate(serverObject,mongoId):
		ServerRequest.tryMainServer()

		serverUrl = ServerRequest.serverUrl
		serverPort = ServerRequest.serverPort

		if not issubclass(serverObject.__class__ ,serverObjects.MongoObject):
			print( "Error {0} is not a mongo object!".format(serverObject))

		if not serverObject.mongoId:
			print( "Error {0} has null id!".format(serverObject))

		serverRes = ServerResponse()
		collection = serverObject.__class__.__name__
		try:
			hdr = {"content-type": "application/json"}
			conn = httpC.HTTPConnection(host = serverUrl, port = serverPort)
			conn.request(method = 'POST', url = '/'+collection+'/'+mongoId, body = json.dumps(serverObject.toDict()), headers = hdr)
			response = conn.getresponse()

			serverRes.header = response.msg 
			serverRes.body = json.loads(response.read().decode('utf-8'))
			serverRes.returnCode = response.status
			serverRes.errorCode = 0
			serverRes.errorMessage = ""
			objectList = [serverObject]
			serverRes.objects = objectList
		except Exception as e:
			serverRes.header = hdr 
			serverRes.body = ""
			serverRes.returnCode = 500
			serverRes.errorCode = 501
			serverRes.errorMessage = AteneaLogger.ErrorHandler.GetErrorMessage(str(serverRes.errorCode),[str(e)])
			
			ServerRequest.serverUrl = ""

		return serverRes

# print(ServerRequest.getToolData("shaders").body)

# sReq = ServerRequest()
# print (sReq.sendToHermes("Message from atenea module!"))

# errorLog = serverObjects.ErrorLogs(user= "toto" ,level = "Critical" ,action = "Export" ,filename = "asd.max" ,errorCode = 20,errorMessage = "tututu")
# data1 =  serverObjects.ExportData(name="asd1",exportType="typ1",exportSubType="sTyp1")
# data2 =  serverObjects.ExportData(name="asd2",exportType="typ2",exportSubType="sTyp2")

# expData =  serverObjects.ExportLogs(user="Juan",filename="asd.max",action="export",command="KUCHUKUCHU",objects=[data1,data2])

# serverObjects.ExportLogs(user= "toto" ,level = "Critical" ,action = "Export" ,filename = "asd.max" ,errorCode = 20,errorMessage = "tututu")


# print(ServerRequest.mongoCreate(expData))
# 
# res = sReq.mongoList(serverObjects.ErrorLogs)
# for obj in res.objects:
# 	print(obj.mongoId)

# res = sReq.mongoList(serverObjects.ExportLogs)
# print(res)


