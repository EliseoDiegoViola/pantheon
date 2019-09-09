from pantheonModules.pantheonUtilities import pantheonHelpers
from pantheonModules.pantheonUtilities import modulesLoader
from pantheonModules.exporter.overrides import *
from imp import reload


reload(modulesLoader)
loader = modulesLoader.ModulesLoader()


class EXPORTABLE_TYPE:
    NONE = -1
    MESH = 0
    COLLIDER = 1
    POINT = 2
    SKELETON = 3
    DUMMY = 4
    SCENE = 5
    MATERIAL = 6
    ANIMATION = 7
    DATA = 8
    DATAMESH = 9

class exportable(object):

    contentType = EXPORTABLE_TYPE.NONE
    objectRepresentation = None
    localOverride = None
    exportableParent = None
    sceneInstance = None

    project = "None"

    def __init__(self,obj,parent,typ):
        platform = pantheonHelpers.getPlatformName()

        self.localOverride = localOverride
        self.objectRepresentation = obj
        self.exportableParent = parent
        self.contentType = typ


    def adoptChild(self,child):
        child.objectRepresentation = self.localOverride.MiscUtilities.SetParent(child.objectRepresentation,self.objectRepresentation)

     