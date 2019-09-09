from .events import *

class ChildLoader(object):
    loaderObject = None
    weight = 0
    

class LoaderObject(object):

    def __init__(self):
        self.onValueUpdated = EventHook()
        self.loaderChildren = []
        self.currentValue = 0
        self.currentMessage = 0

    def __repr__(self):
        return "{0} : {1} progress with {2} message".format(id(self),self.currentValue,self.currentMessage)

    def __nonzero__(self):
        return True 

    def connectLoader(self,other,weight):
        if isinstance(other,LoaderObject):
            child = ChildLoader()
            child.loaderObject = other
            child.weight = weight
            child.loaderObject.onValueUpdated += lambda : self.updateChildProgress(child)

            self.loaderChildren.append(child)

            if child.loaderObject.currentValue > 0:
                self.updateChildProgress(child)
        else:
            raise Exception("The second parameter should be a LoaderObject, recieved {0}".format(other))

    def disconnectLoader (self,loader):
        myChild = next([c for c in self.loaderChildren if c.loaderObject == loader],None)
        if myChild:
            myChild.loaderObject.onValueUpdated = EventHook()
            self.loaderChildren.remove(myChild)


    def updateChildProgress(self,child):
        totalWeight = sum([c.weight for c in self.loaderChildren])
        realProgress = sum([c.loaderObject.currentValue / totalWeight for c in self.loaderChildren])
        self.currentValue = realProgress
        if child.loaderObject.currentMessage:
            self.currentMessage = child.loaderObject.currentMessage

        self.onValueUpdated()


    def reportProgress(self,value,msg = ""):

        if self.loaderChildren : raise Exception(" You cant report progress directly when you have children ")
        if value > 1 or value < 0: raise Exception("Report progress value must be between 0 and 1, recieved {0}".format(value))
        if msg: self.currentMessage = msg
        self.currentValue = value
        self.onValueUpdated()


#TESTING
# masterLo = LoaderObject()
# masterLo.onValueUpdated += lambda : print(str(masterLo) + " MASTER ")
# mainLo = LoaderObject()
# mainLo.onValueUpdated += lambda : print(str(mainLo) + " MAIN ")
# mainLo2 = LoaderObject()
# mainLo2.onValueUpdated += lambda : print(str(mainLo2) + " MAIN ")
# masterLo.connectLoader(mainLo,1)
# masterLo.connectLoader(mainLo2,1)
# cl1 = LoaderObject()
# cl2 = LoaderObject()
# cl3 = LoaderObject()
# mainLo.connectLoader(cl1,1)
# mainLo.connectLoader(cl2,1)
# mainLo2.connectLoader(cl3,1)
# cl1.reportProgress(0.5,"cl1 test")
# cl2.reportProgress(0.5,"cl2 test")
# cl3.reportProgress(0.5,"cl3 test")