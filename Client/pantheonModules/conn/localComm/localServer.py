#PYTHON 3 ONLY
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import threading
from pantheonModules.pantheonUtilities import events
from pantheonModules.pantheonUtilities import loader
from PyQt5.QtCore import QThread, pyqtSignal


# class myClassA(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#         self.daemon = True
#         self.pr = progressReport()
#         self.start()

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

class LocalServer(QThread):
    onProgressReported = pyqtSignal(object)
    onFileExported = pyqtSignal(str)
    onErrorFound = pyqtSignal(object)

    def __init__(self,port):
        QThread.__init__(self)
        self.server = SimpleXMLRPCServer(("localHost",port),requestHandler=RequestHandler,allow_none=True)
        self.server.register_introspection_functions()
        self.functions = {}
        self.instances = {}

        self.server.register_function(self.emitProgress, "emitProgress")
        self.server.register_function(self.emitExport, "emitExport")
        self.server.register_function(self.emitError, "emitError")

    def emitProgress(self,loaderObject):
        self.onProgressReported.emit(loaderObject)

    def emitExport(self,val):
        self.onFileExported.emit(val)

    def emitError(self,criticalException):
        self.onErrorFound.emit(criticalException)


    def addFunction(self,function,eventName):
        if eventName not in self.functions:
            self.functions[eventName] = events.EventHook()

        self.functions[eventName] += function
        self.server.register_function(self.functions[eventName], eventName)

    def addInstance(self,instance):
        self.server.register_instance(instance)

    def run(self):
        print("RUNNING!")
        self.server.serve_forever()


        

# class progressReport():
#     prog = 0
#     callback = None
#     def reportProgress(self,add=None,absolute=None):
#         if add:
#             self.prog = self.prog + add
#         if absolute:
#             self.prog = absolute
#         if self.callback:
#             self.callback()
#         return self.prog

# def printData(data):
#     print(data)
# pr = progressReport()
# localServer = LocalServer(8000)
# localServer.addInstance(pr)
# localServer.start()
# pr.callback = lambda : printData(pr.prog)
# print(pr.reportProgress(1))

# with LocalServer(8000) as server:
#     a = myClassA()
#     print (a.pr.reportProgress(1))
#     # server.addFunction(reportProgress,"reportProgress")
#     server.addInstance(a.pr)
#     server.startServer()
# Create server
# if python3:
#     with SimpleXMLRPCServer(("localhost", 8000),
#                             requestHandler=RequestHandler) as server:
#         server.register_introspection_functions()

#         # Register pow() function; this will use the value of
#         # pow.__name__ as the name, which is just 'pow'.
#         server.register_function(pow)

#         # Register a function under a different name
#         def adder_function(x,y):
#             return x + y
#         server.register_function(adder_function, 'add')

#         # Register an instance; all the methods of the instance are
#         # published as XML-RPC methods (in this case, just 'mul').
#         class MyFuncs:
#             def mul(self, x, y):
#                 return x * y

#         server.register_instance(MyFuncs())

#         # Run the server's main loop
#         server.serve_forever()
# else:
#     try:
#         server = SimpleXMLRPCServer(("localhost", 8000),requestHandler=RequestHandler)
#         server.register_introspection_functions()

#         # Register pow() function; this will use the value of
#         # pow.__name__ as the name, which is just 'pow'.
#         server.register_function(pow)

#         # Register a function under a different name
#         def adder_function(x,y):
#             return x + y
#         server.register_function(adder_function, 'add')

#         # Register an instance; all the methods of the instance are
#         # published as XML-RPC methods (in this case, just 'mul').
#         class MyFuncs:
#             def mul(self, x, y):
#                 return x * y

#         server.register_instance(MyFuncs())

#         # Run the server's main loop
#         server.serve_forever()
#     except Exception as e:
#         print e