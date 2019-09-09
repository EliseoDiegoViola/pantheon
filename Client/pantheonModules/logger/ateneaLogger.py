import os
import sys
import json
from time import gmtime, strftime

import ctypes  # An included library with Python install.

errorCodes = {
    "000": "Success",
    "001": "Not implemented in override",
    "002": "No jsonmeta files found!",
    "100": "--ERROR: Cannot attach {0} with {1}",    
    "101": "--ERROR: Parent: <{0}> | Without children",
    "102": "--ERROR: Parent: <{0}> | Without editable poly as children",
    "103": "--ERROR: Parent: <{0}> | Child <{1}> is not an editable poly",
    "104": "--ERROR: MERGE EXCEPTION - Cannot attach {0} with {1}",
    "200": "--ERROR: EZMats file not found, dont forget to use the tool before exporting :)",
    "201": "--ERROR: Parent: <{0}> | Without attributes, add type and subtype before export",
    "300": "--ERROR: Parent: <{0}> | Has an instanced child <{1}>. Children can't be Instances",
    "400": "--ERROR: Parent: <{0}> | Has to be Helper",
    "500": "--ERROR: Texture not present in server: {0}",
    "501": "--ERROR: Server Bad Request: {0}",
    "600": "--ERROR: Parent: <{0}> | Mesh <{1}> doesn't use all ID's defined in Material <{2}>. Check material usage on this mesh",
    "601": "--ERROR: Parent: <{0}> | Mesh <{1}> has a face <{2}> with a material ID not defined"

}

debugPath = ""

class AteneaLogger():

    # class __AteneaLogger:
        
    #     def __init__(self):
            
    #     def ilog(self,val):
    #         with open(self.debugPath, "a+") as logFile:
    #             logFile.write(strftime("%m/%d/%Y %H:%M:%S %p", gmtime()) + "+-++-+" +str(val)+"\n")

    # instance = None
    @staticmethod
    def getDebugPath():
        global debugPath

        if not debugPath:
            if( os.path.exists(os.path.expanduser('~/Documents/'))):
                debugPath = os.path.expanduser('~/Documents/') + "Export.log"
            else:
                debugPath = os.path.expanduser('~/') + "Export.log"

        return debugPath
    

    # def __new__(cls): #__new__ always a classmethod
    #     if not AteneaLogger.instance:
    #         AteneaLogger.instance = AteneaLogger.__AteneaLogger()
    #     return AteneaLogger.instance


    # def __init__(self):
    #     if( os.path.exists(os.path.expanduser('~/Documents/'))):
    #         self.debugPath = os.path.expanduser('~/Documents/') + "Export.log"
    #     else:
    #         self.debugPath = os.path.expanduser('~/') + "Export.log"

    @staticmethod
    def log(val):
        print(str(val))
        debug = AteneaLogger.getDebugPath()
        with open(debug, "a+") as logFile:
            logFile.write(strftime("%m/%d/%Y %H:%M:%S %p", gmtime()) + "+-++-+" +str(val)+"\n")

    @staticmethod
    def logException(errorCode,*args):
        val = AteneaLogger.ErrorHandler.GetErrorMessage(errorCode,*args)
        print(val)
        debug = AteneaLogger.getDebugPath()
        with open(debug, "a+") as logFile:
            logFile.write(strftime("%m/%d/%Y %H:%M:%S %p", gmtime()) + "+-++-+" +str(val)+"\n")

    # def log(self,val):
    #     print(str(val))
    #     with open(self.debugPath, "a+") as logFile:
    #         logFile.write(strftime("%m/%d/%Y %H:%M:%S %p", gmtime()) + "+-++-+" +str(val)+"\n")

    # def logException(self,errorCode,*args):
    #     val = ErrorHandler.GetErrorMessage(errorCode,*args)
    #     print(val)
    #     with open(self.debugPath, "a+") as logFile:
    #         logFile.write(strftime("%m/%d/%Y %H:%M:%S %p", gmtime()) + "+-++-+" +val+"\n")

    class ErrorHandler():

        @staticmethod
        def GetErrorMessage(errorCode, args):
            global errorCodes
            return errorCodes[errorCode].format(*args)

    class ErrorStack():
        def __init__(self):
            self.errorStack = []

        def hasErrors(self):
            return len(self.errorStack) > 0

        def addErrorMessage(self, error):
            self.errorStack.append(error)

        def addError(self, errorcode,args = []):
            error = AteneaLogger.ErrorHandler.GetErrorMessage(errorcode,args)
            self.errorStack.append(error)

        def addSeparator(self):
            self.errorStack.append("--------------------------")

        def showMessageBox(self, title, text, style): #Convert to QT
            return ctypes.windll.user32.MessageBoxW(0, text, title, style)        

        def getErrorMsg(self):

            errorStr = ""
            for error in self.errorStack:
                errorStr += error + "\n"
            return errorStr