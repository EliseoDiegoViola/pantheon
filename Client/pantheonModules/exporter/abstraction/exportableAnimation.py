from .exportable import *
from .animationEvent import *
from pantheonModules.pantheonUtilities import events


class exportableAnimation():
    
    clipName = None
    startKey = -1
    endKey = -1
    isLoop = False
    isRoot = False

    events = []
    # OnPropertiesChanged = None


    def __init__(self):
        pass
        # super(exportableAnimation,self).__init__(baseNode,parent,typ)
        # self.OnPropertiesChanged = events.EventHook()

    def __repr__(self):
        return 

    def __hash__(self):
        return hash(str(self))

    def __eq__(self,other):
        return str(self) == str(other)

    
