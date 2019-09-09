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

import os
import sys
import json
from time import gmtime, strftime

from multiprocessing.connection import Listener


class Logger():

    def __init__(self):
        if( os.path.exists(os.path.expanduser('~/Documents/'))):
            self.debugPath = os.path.expanduser('~/Documents/') + "Export.log"
        else:
            self.debugPath = os.path.expanduser('~/') + "Export.log"

    def log(self,val):
        print(val)
        with open(self.debugPath, "a+") as logFile:
            logFile.write(strftime("%m/%d/%Y %H:%M:%S %p", gmtime()) + "+-++-+" +val+"\n")

# from pantheonModules.versioning import requests
# from pantheonModules.pantheonUtilities import iniConfig

# def log(message):
#     print(message)
#     with open(ateneaLog, "a+") as myfile:
#         myfile.write(strftime("%m/%d/%Y %H:%M:%S %p", gmtime()) + "++++++"+message+"\n")


class Batching():

    def __init__(self):
        self.mockUpsTypes = ['/**/*.fbx']
        self.rigTypes = ['/**/*.mb','/**/*.ma']
        
        self.args = self.parseArguments()
        self.rigName = None
        if self.args.rig != None:
            self.rigName = self.args.rig

        self.workingPaths = self.initWorkingPaths()
        self.commandLines = self.getCommandsTemplate()
        self.logger = Logger()
        self.address = ('localhost', 6000)     # family is deduced to be 'AF_INET'
        self.listener = Listener(self.address, authkey=b'batch')


    def ProcessExport(self):
        args = self.args

        self.logger.log("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        self.logger.log("++++++STARTING PYTHON PROCESS++++++++")
        self.exportMocap()
        self.logger.log("++++++FINISHED PYTHON PROCESS++++++++")


    def parseArguments(self):
        parser = argparse.ArgumentParser(description='Batch process to import a mockup to a RIG.')
        parser.add_argument('-r', '--rig', help='The name of the rig to be processed')        
        # parser.add_argument('-s','--step', type=int , help='The step of the process you want to start from. \n 1 - All \n 2 - Only build avatars', default=-1)
        # parser.add_argument('-i','--input', nargs='+', help='The input for the script should be 1 or 2 arguments in the form of \'-i folder\' or \'-i folder assetname\'',default=[])
        # parser.add_argument('-z','--zip', nargs='?',const=True,help='Zip all output files and returns the zip directory instead of taking them to the unity project.',default=False)
        # parser.add_argument('-o','--overwrite', nargs='?',const=True,help='Overwrite all textures and files, and bypass the name check',default=False)
        # parser.add_argument('-v','--verbose',nargs='?', type=int ,const=1,help='Verbose level.',default=0)

        return parser.parse_args()

    def initWorkingPaths(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        workingPaths = {} 

        builderIni = dir_path + "/BatchConfig.json"
        with open(builderIni) as data_file:    
            workingPaths = json.load(data_file)

        #CORRECT WORKING PATHS
        scriptPath = dir_path + "/MockUpScriptNew.py"
        print("SCRIPTPATH: ", scriptPath)
        workingPaths["scriptPath"] = scriptPath

        return workingPaths

    def getCommandsTemplate(self):
        commandLines= {}
        #0 -> Program Path
        #1 -> scriptPath
        #2 -> FilePath

        commandLines[".fbx"] = '{0} {1} {2} {3}'
        # commandLines[".ma"] = '{0} {1} {2}'
        # commandLines[".3ds"] = '{0} -q -silent -mip -mxs  "python.executeFile @\\\"{1}\\\"; quitMAX() #nopromptfile.max" {2}'
        # commandLines[".max"] = '{0} -q -silent -mip -mxs  "python.executeFile @\\\"{1}\\\"; quitMAX() #nopromptfile.max" {2}'
        # commandLines[".blend"] = '{0} -b {2} -P {1}'

        return commandLines 

    def fetchFiles(self,dirPath,types):
         
        onlyfiles = []
        if os.path.isdir(dirPath):
            for ftype in types:
                onlyfiles.extend(glob.glob(dirPath+ftype,recursive=True))
        return onlyfiles

    def exportMocap(self):
        if self.rigName == None:
            self.logger.log("Error: NO RIG NAME SPECIFIED, RETURNING")
            return

        self.logger.log("++++++Fetching requested files++++++++")

        validProcess = False
        
        onlyfiles = self.fetchFiles(os.path.dirname(os.path.realpath(__file__))+"/Mocks/",self.mockUpsTypes)
        onlyfiles = [w.replace('\\', '/') for w in onlyfiles]
        self.logger.log("++++++Found "+ str(len(onlyfiles)) +" Files++++++++")
        
    
        self.logger.log('Processing Files\n' + '\n'.join(onlyfiles))
        
        # fileType = file.replace('\\','/').replace(artistsPlaticPath, "").split('/')[0]
        # filePath = file.replace('\\','/')
        # filePath = fileType+"/"+ os.path.dirname(filePath).split("/")[len(os.path.dirname(filePath).split("/"))-1]

        fileExtension = ".fbx"

        command = self.commandLines[fileExtension].format(self.workingPaths["mayaPath"],self.workingPaths["scriptPath"], self.rigName,'"'+'" "'.join(onlyfiles)+'"')

        print("===============")
        print("COMMAND:", command)
        print("===============")        

        program = subprocess.Popen(command) #stdout=subprocess.PIPE,stderr=subprocess.PIPE,
        print("PROCESS STARTED")
        # out,err = program.communicate()
        # exitcode = program.returncode
        
        # if str(exitcode) != '0':
        #     self.logger.log(err.decode("utf-8") )
        #     self.logger.log(out.decode("utf-8") )
        #     self.logger.log('error opening file')
        # else:
        #     programoutput = out.decode("utf-8").split('\n')
        #     programoutput = list(filter(None, programoutput)) # fastest
        #     print(out.decode("utf-8"))
        
        conn = self.listener.accept()
        print ('connection accepted from {0}'.format(self.listener.last_accepted))

        while True:
            msg = conn.recv()
            print(msg)
            if msg == 'FINISHED':
                conn.close()
                break

        self.listener.close()
        
        return validProcess

   


    



atenea = Batching()
atenea.ProcessExport()
