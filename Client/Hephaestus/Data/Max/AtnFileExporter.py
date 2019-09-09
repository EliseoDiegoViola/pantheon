import MaxPlus
import json
import urllib2 as url
import os
import copy
from PySide import QtGui,QtCore
from sets import Set
import sys
#from pantheonModules import pantheonUtilities
from pantheonModules.pantheonUtilities import modulesLoader
reload(modulesLoader)
loader = modulesLoader.ModulesLoader()

class AteneaExporter():

    output = ""


    def __init__(self):
        ateneaLogger = loader("pantheonModules.logger.ateneaLogger")
        MAXOverrides = loader("pantheonModules.overrides.MAXOverrides")

        self.logger = ateneaLogger.AteneaLogger()
        self.meshUtilities = MAXOverrides.MAXMeshesUtilities()
        self.layerUtilities = MAXOverrides.MAXLayersUtilities()  
        self.exportUtilities = MAXOverrides.MaxExportUtilities()
        self.dataParser = MAXOverrides.MAXDataParser()
        self.fileUtilities = MAXOverrides.MAXFileUtilities()
        
        self.layerUtilities.cleanGarbageLayer()
        self.output = self.fileUtilities.GetFullFileName()
        print self.output

    def exportAtn(self):
        meshesOrder = self.meshUtilities.reorderMeshes()
        exportLayers = self.layerUtilities.loadAllLayerNames()
        
        childs = self.layerUtilities.selectObjectsInLayers(exportLayers)
        
        for child in childs:
            
            data  = self.dataParser.parseDataObject(objToParse=child,output=self.output)
            self.exportUtilities.exportFBX(self.output+child.GetName(),child)

            json_data = json.dumps(data)
            with open(self.output+child.GetName()+".jsonmeta", "w+") as text_file:
                    text_file.write(json_data)

            sys.stdout.write("|OUTPUTFILE|"+self.output+child.GetName()+".fbx\n")
            sys.stdout.write("|OUTPUTFILE|"+self.output+child.GetName()+".jsonmeta\n")
        return True
 
if __name__ == '__main__':
    objExporter = AteneaExporter()
    objExporter.exportAtn()
    


    
    
    
            # data = {}
            # data["data"] = materialsData
            # data["obj"] = objData
            # data["matOrder"] = meshesOrder # OPTIMIZE!

    # for node in MaxPlus.Core.GetRootNode().Children:
           
        #     nodeAttr = self.dataParser.nodeAttribute(node.GetName(),'ObjectBaseData')
        #     nodeAttr.addCustomParameter('type','Piece')
        #     nodeAttr.addCustomParameter('subtype','Horizontal')