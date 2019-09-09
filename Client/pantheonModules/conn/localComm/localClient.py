import socket
try:
    import xmlrpc.client as xmlRPC
except Exception:
    import xmlrpclib as xmlRPC
from pantheonModules.logger.ateneaLogger import AteneaLogger
server = None
port = 49241
def emitProgress(loaderObject):
    global server
    try:
        if server is None: 
            server = xmlRPC.ServerProxy('http://localhost:'+str(port),allow_none=True)
        server.emitProgress(loaderObject)
    except socket.error:
        print("Athenea Core is not running")

def emitExport(errormsg):
    global server
    try:
        if server is None: 
            server = xmlRPC.ServerProxy('http://localhost:'+str(port),allow_none=True)
        server.emitExport(errormsg)
    except socket.error:
        print("Athenea Core is not running")

def emitError(errorException):
    global server
    try:
        if server is None: 
            server = xmlRPC.ServerProxy('http://localhost:'+str(port),allow_none=True)

        server.emitError(errorException)
    except socket.error:
        print("Athenea Core is not running")

# emitError("asd.max","During merge","Box001 is not a Poly")





# s = xmlRPC.ServerProxy('http://localhost:8000')
# print(s.system.listMethods())
# # print(s.pow(2,3))  # Returns 2**3 = 8
# print(s.reportProgress(1))  # Returns 5
# # print(s.mul(5,2))  # Returns 5*2 = 10

# Print list of available methods
# print(s.system.listMethods())

# reportError("TEST")