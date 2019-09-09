#####################################################
#               ANIMATION FIXER                     #
#####################################################


import json
import urllib2 as url #Hello Python 2!
import os
import copy
from sets import Set
import sys
#from pantheonModules import pantheonUtilities
from pantheonModules.pantheonUtilities import modulesLoader
from pantheonModules.pantheonUtilities import pantheonHelpers
reload(modulesLoader)
loader = modulesLoader.ModulesLoader()


consoleOut = sys.__stdout__
consoleError = sys.__stderr__

import traceback

class AteneaExporter():

    fileUtilities = None
    miscUtilities = None
    filesToOpen = None
    meshUtilities = None
    animationUtilities = None
    layerUtilities = None
    exportUtilities = None
    callBackUtilities = None
    output = None
    dataParser = None

    def __init__(self):
        self.ateneaLogger = loader("pantheonModules.logger.ateneaLogger")
        self.logger = self.ateneaLogger.AteneaLogger()

        self.logger.log("STARTING ATENEA EXPORTER")

        platform = pantheonHelpers.getPlatformName()

        fileToOpen = ""
        if platform == pantheonHelpers.MAX_2018_NAME():
            self.localOverride = loader("pantheonModules.exporter.overrides.MAXOverrides")
        elif platform == pantheonHelpers.MAYA_NAME():
            self.localOverride = loader("pantheonModules.exporter.overrides.MAYAOverrides") 
        elif platform == pantheonHelpers.BLENDER_NAME():
            self.localOverride = loader("pantheonModules.exporter.overrides.BLENDEROverrides")        
        
        self.fileUtilities = self.localOverride.FileUtilities #static class
        self.miscUtilities = self.localOverride.MiscUtilities #static class

        self.logger.log("--------------- ABOUT TO READ" )

        self.filesToOpen = self.localOverride.FileUtilities.GetFileArguments() #
        self.logger.log("---------------" + str(self.filesToOpen))

    def updateUtilities(self):
        
        self.meshUtilities = self.localOverride.MeshesUtilities()
        self.layerUtilities = self.localOverride.LayersUtilities()
        self.exportUtilities = self.localOverride.ExportUtilities()
        

    def cleanup(self):
        print("CLEAN!")
        if self.callBackUtilities:
            self.callBackUtilities.clean()

        self.output = None
        self.meshUtilities = None
        self.animationUtilities = None
        self.layerUtilities = None
        self.exportUtilities = None
        self.dataParser = None
        self.callBackUtilities = None

    def fixFile(self,file):
        self.logger.log("----------ABOUT TO OPEN---------")

        if file:
            self.fileUtilities.OpenFile(file)
        else:
            file = self.fileUtilities.GetFullFileName()

        self.logger.log("----------DATA PARSER!---------")
        self.dataParser = self.localOverride.DataParser(self.localOverride.FileUtilities.GetFullFileName())
        self.logger.log("----------ABOUT TO LAYER READ---------")
        exportLayers = self.layerUtilities.loadAllLayerNames()
        self.logger.log("----------ABOUT TO SELECT OBJECT---------")
        parents = self.layerUtilities.selectObjectsInLayers(exportLayers,add = False)

        self.logger.log("----------ABOUT CHILD---------")
        for child in parents :
            nodeAttr = self.dataParser.nodeAttribute(child,'ObjectBaseData')
            nodeAttr.addCustomParameter('type','Animation')
            nodeAttr.addCustomParameter('subtype','Biped')
        

        self.fileUtilities.SaveFile(file)
        self.logger.log("----------FIX FINISHED---------")


    def fixJsonAnim(self):
        self.logger.log("----------DATA---------")
        output = self.fileUtilities.GetFullFileName()
        with open(output+'.jsonAnim') as data_file:
             animData = json.load(data_file)
             if('animations' in animData):
                clipDatas = animData['animations']
                clipDatas[0]["clipName"] = os.path.basename(output)
        json_data = json.dumps(animData)    
        with open(output+".jsonAnim", "w+") as text_file:
            text_file.write(json_data)

if __name__ == '__main__':
    try:
        if objExporter:
            objExporter.cleanup()
    except NameError:
        print("First Run")

    
    objExporter = AteneaExporter()
    if objExporter.filesToOpen:
        for file in objExporter.filesToOpen:
            objExporter.updateUtilities()
            objExporter.logger.log("------------------ FILE: " + file)
            objExporter.fixFile(file)
            objExporter.fixJsonAnim()
            objExporter.cleanup()
    else:
        objExporter.updateUtilities()
        objExporter.fixFile(None)
        objExporter.fixJsonAnim()
        objExporter.cleanup()


    # for node in MaxPlus.Core.GetRootNode().Children:
           
        #     nodeAttr = self.dataParser.nodeAttribute(node.GetName(),'ObjectBaseData')
        #     nodeAttr.addCustomParameter('type','Piece')
        #     nodeAttr.addCustomParameter('subtype','Horizontal')