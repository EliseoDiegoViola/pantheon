import os
import sys
import subprocess

import argparse
import glob
import shutil

import zipfile
import json

from collections import namedtuple

import tempfile
import imp

from PyQt5.QtCore import QProcess 
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox

from UI import MainWindow


from pantheonModules.ui.windows import popup
from pantheonModules.conn.localComm import localServer
from pantheonModules.pantheonUtilities import loader ,events , fileSystemUtilities as fsu , iniConfig
from pantheonModules.logger import ateneaLogger






class AteneaCore(QApplication):

    reportProgress = None
    logConsole = None

    def __init__(self):
        super().__init__([])

        self.logConsole = events.EventHook()
        self.reportProgress = events.EventHook()

        self.logger = ateneaLogger.AteneaLogger()
        self.errorStack = ateneaLogger.AteneaLogger.ErrorStack()

        self.logConsole += self.logger.log

        self.logConsole("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        
        #self.versioningRequest = requests.Requests()
        self.exportTypes = ('/**/*.ma','/**/*.mb','/**/*.blend','/**/*.max','/**/*.3ds')
        # self.args = self.parseArguments()

        self.buildINIPaths = self.initWorkingPaths()
        self.commandLines = self.getCommandsTemplate()

        
        
        self.mainWindow = MainWindow.ShowUI(
            step1Callback = self.runExportProcess,
            step2Callback = self.runEngineProcess,
            logConsoleEvent = self.logConsole,
            progressReportEvent = self.reportProgress,
            settingsUpdated = self.reloadInitPaths
            )

        self.mainWindow.show()
        self.mainWindow.projectSettingsLoaded += self.setCurrentProjectSettings

        self.reportProgress(0,"")

    def reloadInitPaths(self):
        self.buildINIPaths = self.initWorkingPaths()

    def initWorkingPaths(self):
        # iniConfig = loader("pantheonModules.pantheonUtilities.iniConfig")
        buildINIPaths = namedtuple('buildINIPaths', 'programs scripts engineExport enginePath projectPath artMasterPath ateneaengineScript')

        pathDocuments= os.path.expanduser('~/Documents/')
        builderIni = pathDocuments + "builder.ini"


        #Check if builder file exists.
        if not os.path.isfile(builderIni):
            arrayFilesOrPrograms=[]
            arrayFilesOrPrograms.append({ "label":"MayaPath", "path":"\\Autodesk\\Maya2017\\bin\\mayapy.exe", "needSearch":True })
            arrayFilesOrPrograms.append({ "label":"MaxPath", "path":"\\Autodesk\\3ds Max 2017\\3dsmax.exe", "needSearch":True })
            arrayFilesOrPrograms.append({ "label":"BlenderPath", "path":"Blender Foundation\\Blender\\blender.exe" , "needSearch":True})
            arrayFilesOrPrograms.append({ "label":"EnginePath", "path":"\\Unity_2017_3\\Editor\\Unity.exe", "needSearch":True })
            arrayFilesOrPrograms.append({ "label":"Exporter", "path":"Projects\\Pantheon\\Client\\pantheonModules\\exporter\\AteneaExporter.py", "needSearch":True })
            arrayFilesOrPrograms.append({ "label":"AteneaEngineScript", "path":"Atenea.ModelImporter.CreateAvatarFromPendingFiles" , "needSearch":False})
            arrayFilesOrPrograms.append({ "label":"EngineExport", "path":"ElementSpace/Artworks/ArtMasters/" , "needSearch":False})
            arrayFilesOrPrograms.append({ "label":"ProjectPath", "path":"Projects\\ElementSpace\\trunk\\Assets\\", "needSearch":True })
            arrayFilesOrPrograms.append({ "label":"ArtMasterPath", "path":"Projects\\ArtMasters\\" , "needSearch":True})
            arrayFilesOrPrograms.append({ "label":"ZipFilePath", "path":"/Temp/LastZip.zip", "needSearch":False })
           
            fsu.createBuilderIni(builderIni,arrayFilesOrPrograms)            

        configFile = iniConfig.AteneaConfig(builderIni) 

        pathsMaps = configFile.getMap("Paths")
        if pathsMaps is None:
            self.logConsole("ERROR - INVALID BUILDER.INI PATH")

        programs = {}
        programs[".mb"] = pathsMaps['mayapath']
        programs[".ma"] = pathsMaps['mayapath']
        programs[".3ds"] = pathsMaps['maxpath']
        programs[".max"] = pathsMaps['maxpath']
        programs[".blend"] = pathsMaps['blenderpath']

        buildINIPaths.programs = programs

        scripts = {}
        scripts[".mb"] = pathsMaps['exporter']
        scripts[".ma"] = pathsMaps['exporter']
        scripts[".3ds"] = pathsMaps['exporter']
        scripts[".max"] = pathsMaps['exporter']
        scripts[".blend"] = pathsMaps['exporter']

        buildINIPaths.scripts = scripts

        
        buildINIPaths.enginePath = pathsMaps['enginepath']
        buildINIPaths.ateneaengineScript = pathsMaps['ateneaenginescript']
        
        return buildINIPaths

    def setCurrentProjectSettings(self,settings):
        self.buildINIPaths.engineExport = settings["paths"]['engineExport']
        self.buildINIPaths.projectPath = settings["paths"]['projectPath']
        self.buildINIPaths.artMasterPath = settings["paths"]['artMasterPath']
        self.mainWindow.projectTitle.setText(settings["projectName"])

        self.allFiles = [FileToBuild(f,self.buildINIPaths.artMasterPath.replace("/","\\")) for f in fsu.fetchFiles(self.buildINIPaths.artMasterPath,self.exportTypes)]
        
        for file in self.allFiles:  #Not the best idea. TODO: Move to somewhere else
           self.checkFileStatus(self.buildINIPaths.projectPath+self.buildINIPaths.engineExport,self.buildINIPaths.artMasterPath,file)

        self.mainWindow.loadFiles(self.allFiles)

    def getCommandsTemplate(self):
        commandLines= {}
        #0 -> Program Path
        #1 -> scriptPath
        #2 -> FilePath

        commandLines[".mb"] = '\"{0}\" {1} fto={2}'
        commandLines[".ma"] = '\"{0}\" {1} fto={2}'

        commandLines[".3ds"] = '\"{0}\" -q -silent  -mxs  \"fto = #({2}); python.executeFile @\\\"{1}\\\";\"' #Should use 3dsmaxcmd.exe?
        commandLines[".max"] = '\"{0}\" -q -silent  -mxs  \"fto = #({2}); python.executeFile @\\\"{1}\\\";\"' #Should use 3dsmaxcmd.exe?
        # commandLines[".max"] = '\"{0}\" -q -silent -mip -mxs \"fto = #({2}); python.executeFile @\\\"{1}\\\"; quitMAX() #nopromptfile.max\"' #Should use 3dsmaxcmd.exe?
        commandLines[".blend"] = '\"{0}\" -b {2} -P {1}'



        #0 -> engine path
        #1 -> Project path
        #2 -> Script Namespace path
        commandLines["engine"] = '\"{0}\"   \'{1}\' -executeMethod {2} -quit -batchmode'

        return commandLines 


    def runExportProcess(self,files,verbose = True):
        self.errorStack = ateneaLogger.AteneaLogger.ErrorStack()
        self.logConsole("++++++Fetching requested files++++++++")
        self.reportProgress(0,"Warming up")
        validProcess = False

        programs = self.buildINIPaths.programs
        scripts = self.buildINIPaths.scripts
        
        self.logConsole("++++++Found "+ str(len(files)) +" Files++++++++")
        oneFileProgress = 0.1/len(files)
        fileExtension = None
        filepaths = []

        for i in range(0,len(files)) :
            file = files[i]
            self.reportProgress((i+1)*oneFileProgress , "Loading {0}".format(file.fileName))
            
            if (verbose):
                self.logConsole('processing ' + file.fullPath)            

            if fileExtension and fileExtension != file.fileExtension:
                self.errorStack.showMessageBox("ERROR", "CANNOT BUILD MULTIPLE FILETYPES IN THIS VERSION")
                return
            
            fileExtension = file.fileExtension
            filepaths.append("\\\"{0}\\\"".format(file.fullPath)  )

        filepathsCommand = ",".join(filepaths)
        command = self.commandLines[fileExtension].format(programs[fileExtension],scripts[fileExtension],filepathsCommand)

        self.reportProgress((i+1)*oneFileProgress , "Opening program  {0}".format(programs[fileExtension]))
        if verbose:
            self.logConsole(command)


        process = QProcess(self)
        process.finished.connect(lambda exitCode, exitStatus: self.exportFinished(process,exitCode, exitStatus,verbose = verbose))
        process.start(command,[])


    def exportFinished(self, process, exitCode, exitStatus, verbose = True):
        print("Exit Status:", exitStatus)
        print("Exit Code:", exitCode)

        programoutput = process.readAllStandardOutput().data().decode("utf-8").split('\n')
        programerror  = process.readAllStandardError().data().decode("utf-8").split('\n')

        if exitCode != 0:
            self.logConsole("".join(programoutput))
            self.logConsole("ERRORS->")
            self.logConsole("".join(programerror))
            self.logConsole("3D PROGRAM CRASHED, NO OUTPUT FILE IS PARSED")                
        else:
            

            if verbose:
                print("OUTPUT")
                print("".join(programoutput))
                print("ERROR")
                print("".join(programerror))

            outputFiles = [k.replace("|OUTPUTFILE|","").replace("\r","") for k in programoutput if '|OUTPUTFILE|' in k]
            
            

            if any(".jsonmeta" in s for s in outputFiles):
                jsonMetaFiles = [s for s in outputFiles if ".jsonmeta" in s]
                fbxFiles = [s for s in outputFiles if ".fbx" in s]
                self.logConsole("Found {0} output files".format(len(jsonMetaFiles)))
                if len(jsonMetaFiles) != len(fbxFiles):
                    log("More Metas than FBXs? ERROR! " + str(len(jsonMetaFiles)) + " -- " + str(len(fbxFiles)))
                    return False
            else:
                jsonMetaFiles = []
                fbxFiles = []


            if len(jsonMetaFiles) > 0:
                for i in range(0,len(jsonMetaFiles)):
                    metaFile = jsonMetaFiles[i]
                    fbxFile = fbxFiles[i]
                    filesToCopy = [metaFile,fbxFile]
                    self.copyExportedFiles(metaFile,filesToCopy)
                    self.logConsole('Step 1 sucessful for '+os.path.splitext(os.path.basename(metaFile))[0])
            else:
                print("Error found in export , copy aborted")

        self.reportProgress(0,"")


    def runEngineProcess(self,files,verbose = True):
        self.logConsole("++++++LOADING engine PROCESS++++++++")

        projectPath = self.buildINIPaths.projectPath
        engineExport = self.buildINIPaths.engineExport
        enginePath = self.buildINIPaths.enginePath

        folder = ""
        asset = ""
        onlyfiles = []
        ftypes = '/*.fbx'

        for file in files :
            engineFilePath = projectPath+engineExport+os.path.dirname(file.relativePath)
            print(engineFilePath+ftypes)
            exportedFiles = glob.glob(engineFilePath+ftypes,recursive=False)

            for expFile in exportedFiles:
                expFile = os.path.splitext(expFile)[0]
                self.logConsole("Creating pending for "+ expFile )
                open(expFile+'.pending', 'w+')

        command = self.commandLines["engine"].format(enginePath,projectPath,self.buildINIPaths.ateneaengineScript)

        self.logConsole(command)
        self.logConsole("Launching engine Process..." )

        process = QProcess(self)
        process.finished.connect(lambda exitCode, exitStatus: self.engineFinished(process,exitCode, exitStatus,verbose = verbose))
        process.start(command,[])


    def engineFinished(self,process,exitCode, exitStatus,outPath = None,verbose = True):

        if exitCode != 0:
            programerror  = process.readAllStandardError().data().decode("utf-8").split('\n')
            self.logConsole("ERROR (engine is already open?)")
            self.logConsole("".join(programerror))
        else:
            programoutput = process.readAllStandardOutput().data().decode("utf-8").split('\n')
            self.logConsole("Step 2 sucessful")
            self.logConsole("".join(programoutput))


    def copyExportedFiles(self,jsonMetaFile,outputFiles):
        self.logConsole("++++++Copying exported files++++++++")

        projectPath = self.buildINIPaths.projectPath
        engineExport = self.buildINIPaths.engineExport
        artMasterspath = self.buildINIPaths.artMasterPath

        engineFileDirectory = projectPath+engineExport
        # texsToCopy,texDB = self.parseMaterials(jsonMetaFile)
        texsToCopy = self.parseMaterials(jsonMetaFile)

        for tex in texsToCopy:
            tex = tex.replace("\\","/")
            if artMasterspath not in tex:
                self.logConsole("{0} not found in artmasters , fix the path ".format(tex))
                continue

            # dest = tex.replace(artMasterspath,projectPath+engineExport)
            dest = projectPath+engineExport+"Textures/"+os.path.basename(tex)
            self.logConsole("Copying file " + tex + "<- TO ->" + dest)
            fsu.copyFile(tex,dest,overwrite=False)
              

        for outFile in outputFiles:
            outFile = outFile.replace("\\","/")
            dest = outFile.replace(artMasterspath,projectPath+engineExport)
            self.logConsole("Copying file " + outFile + "<- TO ->" + dest)
            fsu.copyFile(outFile,dest,overwrite=True)

    def parseMaterials(self,metaPath):
        startDir = os.path.dirname(metaPath)
        with open(metaPath) as data_file:    
            data = json.load(data_file)
            texturesToCopy = []
            # texturesDataDb = {}
            if "materials" in data:
                self.logConsole("Reading Texture list from " + metaPath)
                mats = data["materials"]
                self.logConsole("Reading materials...")
                
                # texturesDataDb["textures"] = {}
                
                for mat in mats:
                    self.logConsole("Parsing material "+mat["name"] +"...")
                    properties = mat["properties"]
                    self.logConsole(str(properties))
                    for prop in properties:
                        if "TexEnv" in prop["propType"] and prop["propValue"]:
                            self.logConsole(str(prop))
                            src_file = fsu.findFileInParents(prop["propValue"],startDir,"/Textures") #os.path.join(src_dir, )
                            if not os.path.exists(src_file):                                
                                self.errorStack.addError("500",[prop["propValue"]])                      
                                continue

                            # dst_dir = destTexturePath

                            # texturesDataDb["textures"][prop["propValue"]] = {}
                            # texturesDataDb["textures"][prop["propValue"]]["references"] = []
                            # texturesDataDb["textures"][prop["propValue"]]["references"].append(mat["name"])

                            texturesToCopy.append( src_file )

                return texturesToCopy#,texturesDataDb

            else:
                self.logConsole("No material in data? ")
                return texturesToCopy#,texturesDataDb
                            

    def checkFileStatus(self,projectPath,artPath,file):
        exportPath = projectPath+os.path.dirname(file.relativePath)+"/" 
        importPath = artPath+os.path.dirname(file.relativePath)+"/"

        if os.path.isfile(exportPath+file.fileName+".prefab"):
            file.UpdateFileStatus(MainWindow.FileStatuses.IMPORTED)
        elif os.path.isfile(importPath+file.fileName+".fbx"):
            file.UpdateFileStatus(MainWindow.FileStatuses.EXPORTED)
        elif os.path.isfile(file.fullPath):
            file.UpdateFileStatus(MainWindow.FileStatuses.ADDED)
        else:
            file.UpdateFileStatus(MainWindow.FileStatuses.UNKNOWN)

    def reportFile(self,value):
        QMessageBox.information(self.mainWindow, "EXPORT"  ,value)

    def reportProg(self,loaderObject):
        print(loaderObject)
        val = loaderObject["currentValue"]
        msg = loaderObject["currentMessage"]
        self.reportProgress(val,msg)

    def reportCrititalError(self,errorException):
        print("ERROR EXCEPTION IS ", errorException)
        msg = QMessageBox(self.mainWindow) 
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Error found while exporting")
        msg.setText("{0} file could not be exported".format(errorException["errorFile"]))
        msg.setInformativeText("Error in {0}".format(errorException["errormessage"]))
        msg.setDetailedText(errorException["errorDetails"])
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

class FileToBuild():

    def __init__(self,filePath,parentPath):

        self.fullPath = filePath
        self.relativePath = filePath.replace(parentPath,"")
        self.fileName = os.path.splitext(os.path.basename(filePath))[0]
        self.fileExtension = os.path.splitext(filePath)[1]
        self.tags = []

        self.OnShowItem = events.EventHook()
        self.OnHideItem = events.EventHook()

        self.OnBuildQueueAdded = events.EventHook()
        self.OnBuildQueueRemoved = events.EventHook()

        self.OnStatusUpdated = events.EventHook()

        self.inBuildList = False
        self.currentStatus =  None

        self.__parsePathIntoTags()

    def __parsePathIntoTags(self):
        splitted = self.relativePath.split("\\")
        self.tags = splitted[:-1]

    def HideItem(self):
        self.OnHideItem(self)
        
    def ShowItem(self):
        self.OnShowItem(self)

    def AddToBuildList(self):
        if not self.inBuildList:
            self.inBuildList = True
            self.OnBuildQueueAdded(self)
        
    def RemoveFromBuildList(self):
        if self.inBuildList:
            self.inBuildList = False
            self.OnBuildQueueRemoved(self)

    def UpdateFileStatus(self,status):
        if isinstance(status,MainWindow.FileStatuses):
            self.currentStatus = status
            self.OnStatusUpdated(self.currentStatus)
        



if __name__ == "__main__":
    core = AteneaCore()
    core.lastWindowClosed.connect((lambda : sys.exit(0)))

    IPCServer = localServer.LocalServer(49241)
    IPCServer.onProgressReported.connect(core.reportProg)
    IPCServer.onFileExported.connect(core.reportFile)
    IPCServer.onErrorFound.connect(core.reportCrititalError)
    IPCServer.start()

    sys.exit(core.exec_())
