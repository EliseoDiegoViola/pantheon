import sys
for module in list(sys.modules):
    if sys.modules[module] and module not in sys.builtin_module_names and "pantheonModules" in str(sys.modules[module]) :
        del(sys.modules[module])
import socket
import re


# from pantheonModules.pantheonUtilities import modulesLoader
# from pantheonModules.pantheonUtilities import pantheonHelpers
from pantheonModules.logger.ateneaLogger import AteneaLogger
from pantheonModules.exporter.overrides import *
from pantheonModules.exporter.abstraction import exportableScene
from pantheonModules.conn.requests import ServerRequest
from pantheonModules.conn import serverObjects
from pantheonModules.conn.localComm import localClient
from pantheonModules.exceptions.exportExceptions import CriticalExportException
from pantheonModules.pantheonUtilities.loader import LoaderObject


import time
start_time = time.time()
# reload(modulesLoader)
# loader = modulesLoader.ModulesLoader()

consoleOut = sys.__stdout__
consoleError = sys.__stderr__
version = 1.26

class AteneaExporter():

    def __init__(self):
        AteneaLogger.log("STARTING ATENEA EXPORTER")
        self.exporterLoader = LoaderObject()
        self.exporterLoader.onValueUpdated += self.reportExportProgress 
        self.fileLoader = {}
        # platform = pantheonHelpers.getPlatformName()

        fileToOpen = ""

        AteneaLogger.log("ABOUT TO READ" )
        self.filesToOpen = localOverride.FileUtilities.GetFileArguments() #
        AteneaLogger.log("FILES > " + str(self.filesToOpen))


        for f in self.filesToOpen:
            AteneaLogger.log("Creating loader for {0}".format(f))
            self.fileLoader[f] = LoaderObject()
            AteneaLogger.log("Connnecting loader for {0}".format(f))
            self.exporterLoader.connectLoader(self.fileLoader[f],1)
        AteneaLogger.log("ARGS PARSED")

    def reportExportProgress(self):
        localClient.emitProgress(self.exporterLoader)

    def exportFile(self,file):
        DEBUG_MODE = False
        AteneaLogger.log("Opening {0}".format(file))
        if file:
            localOverride.FileUtilities.OpenFile(file)
        else:
            DEBUG_MODE = True
            file = localOverride.FileUtilities.GetFullFileName()

            localOverride.MiscUtilities.ImportReferences()
        
        localOverride.LayersUtilities.CleanGarbageLayer()

        print("time elapsed: {:.2f}s".format(time.time() - start_time))
    
        AteneaLogger.log("INIT SCENE!")
        scene = exportableScene.exportableScene(file)
        print("time elapsed: {:.2f}s".format(time.time() - start_time))
        if file in self.fileLoader:
            scene.sceneLoader = self.fileLoader[file]
        print("time elapsed: {:.2f}s".format(time.time() - start_time))
        AteneaLogger.log("PARSING SCENE!")
        scene.parseScene()
        print("time elapsed: {:.2f}s".format(time.time() - start_time))
        if DEBUG_MODE:
            scene.drawTree()

        # validScene = scene.validateScene() Assume that is valid
        AteneaLogger.log("PREPARE EXPORTABLE")
        scene.prepareExportableObjects()
        print("time elapsed: {:.2f}s".format(time.time() - start_time))
        AteneaLogger.log("EXPORTING...")
        # return 
        if DEBUG_MODE:
            scene.drawTree()
        
        for exportableParent in scene.exportableParents:
            data = scene.parseExportDataObject(exportableParent)
            data["version"] = version

            outputFiles = scene.exportObject(exportableParent,data)
            for out in outputFiles:
                AteneaLogger.log("WRITING OUTPUT " + out)
                consoleOut.write(out)


        print("time elapsed: {:.2f}s".format(time.time() - start_time))
        AteneaLogger.log("----------EXPORT FINISHED---------")
        return scene


#EXPORTDATA name="asd1",exportType="typ1",exportSubType="sTyp1"
#EXPORT user="Juan",filename="asd.max",action="export",command="KUCHUKUCHU",objects=[data1,data2]
#ERROR user= "toto" ,level = "Critical" ,action = "Export" ,filename = "asd.max" ,errorCode = 20,errorMessage = "tututu"
def saveExportLog(parsedScene):
    AteneaLogger.log("ABOUT TO SAVE DATA IN SERVER!")
    try:
        filename = str(parsedScene)
        exportDatas = []
        userName = socket.gethostname()
        action = "export"
        command = "".join(sys.argv)

        for expoP in parsedScene.exportableParents:
            exportData = serverObjects.ExportData(name=str(expoP),exportType=expoP.objectType,exportSubType=expoP.objectSubType)
            exportDatas.append(exportData)

        exportLog = serverObjects.ExportLogs(user=userName,filename=filename,action=action,command=command,objects=exportDatas)

        ServerRequest.mongoCreate(exportLog)
    except Exception as e:
        errorSpace = " ".join(re.findall('[A-Z][^A-Z]*',saveExportLog.__name__)).lower()
        raise CriticalExportException(filename,errorSpace,"Error Saving export data in server, call a developer to help you, or export in offline mode (WIP)")
    AteneaLogger.log("DATA SAVED!")





if __name__ == '__main__' or __name__ == "SublimeBlender": # "SublimeBlender" is for testing purposes
    try:
        objExporter = AteneaExporter()
        
        if objExporter.filesToOpen:
            for file in objExporter.filesToOpen:
                # objExporter.updateUtilities()
                AteneaLogger.log(file)
                parsedScene = objExporter.exportFile(file)
                saveExportLog(parsedScene)
        else:
            file = None
            parsedScene = objExporter.exportFile(file)
            saveExportLog(parsedScene)
        # objExporter.localOverride.MiscUtilities.Exit(0)
    except CriticalExportException as cee:
        AteneaLogger.log("Exception!")
        AteneaLogger.log("Critical error on {0} error in {1} {2}".format(cee.errorFile,cee.errormessage,cee.errorDetails))
        #localClient.emitError(cee)

        # consoleError.write("\n EXCEPTION!\n EXCEPTION!\n EXCEPTION!\n EXCEPTION!\n EXCEPTION!\n EXCEPTION!\n EXCEPTION!\n EXCEPTION!\n EXCEPTION!\n EXCEPTION!")
        # consoleOut.write("\n EXCEPTION11111!\n EXCEPTION11111!\n EXCEPTION11111!\n EXCEPTION11111!\n EXCEPTION11111!\n EXCEPTION11111!\n EXCEPTION11111!\n EXCEPTION11111!\n EXCEPTION11111!\n EXCEPTION11111!")
        
        # objExporter.localOverride.MiscUtilities.Exit(1)


