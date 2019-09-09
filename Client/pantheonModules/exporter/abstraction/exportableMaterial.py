import copy

from .exportable import *
from pantheonModules.pantheonUtilities import events
from pantheonModules.conn import serverObjects


class exportableMaterial(exportable):

    #engineShader = None
    #shaderProperties = None
    OnPropertiesChanged = None
    serverMaterial = None


    def __init__(self,baseNode,parent,typ):
        super(exportableMaterial,self).__init__(baseNode,parent,typ)
        self.OnPropertiesChanged = events.EventHook()

    def __repr__(self):
        return self.localOverride.MiscUtilities.GetObjectName(self.objectRepresentation)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self,other):
        return str(self) == str(other)

    def setServerMaterial(self,sMaterial):
        self.serverMaterial = sMaterial
        self.OnPropertiesChanged(self)


    # def setEngineShader(self, shader, defaultProperties):
    #     self.engineShader = copy.deepcopy(shader)
    #     self.shaderProperties = copy.deepcopy(defaultProperties)
    #     self.OnPropertiesChanged(self)

    def editProperty(self,propertyName,newValue):
        props = [prop for prop in self.serverMaterial.properties if prop.propName == propertyName]
        if len(props) != 1:
            print("{0} property was not found in this shader".format(propertyName))
            return False
        else:
            prop = props[0]
            prop.propValue = newValue
            self.OnPropertiesChanged(self)
            return True
            

    def deleteProperty(self,propertyName):
        prop = next(iter([prop for prop in self.serverMaterial.properties if prop.propName == propertyName]),None)
        if not prop:
            print("{0} property was not found in this shader".format(propertyName))
            return False
        else:
            self.serverMaterial.properties.remove(prop)
            self.OnPropertiesChanged(self)
            return True
            

    def getPropertyByname(self,propertyName):
        props = [prop for prop in self.serverMaterial.properties if prop.propName == propertyName]
        if len(props) != 1:
            print("{0} property was not found in this shader".format(propertyName))
            return None
        else:
            prop = props[0]
            return prop.propValue
        
    def getAllProperties(self):
        if self.serverMaterial and self.serverMaterial.properties:
            props = [prop for prop in self.serverMaterial.properties if prop.propValue and prop.propValue != "None" ]
            return props        
        else:
            return []

    def getAssignedTextures(self):
        mapsList = self.localOverride.MiscUtilities.GetMaterialMaps(self.objectRepresentation)
        mapsList.sort()
        return mapsList

    # def getAssignedEmissiveColor(self):
    #     mapsList = self.localOverride.MiscUtilities.GetMaterialMaps(self.objectRepresentation)
    #     mapsList.sort()
    #     return mapsList

    def deleteMaterial(self):
        self.localOverride.MiscUtilities.DeleteMaterial(self.objectRepresentation)

    def hasPropertiesDefined(self):
        props =  [prop for prop in self.serverMaterial.properties if prop.propValue and prop.propValue != "None" ]
        if props:
            return True
        else:
            return False


