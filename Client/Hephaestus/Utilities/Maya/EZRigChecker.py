#from PySide import QtGui,QtCore #FIX THIS !!!!!!

import sys
import json
import urllib2 as url
import os
import copy
from sets import Set
import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel

EzRigCheckerEditorWindowTitle = "EzRigChecker 0.3"

class EzRigCheckerEditor(object):    

    def __init__(self):
        print "Initialized"

    def show(self):
        self.window.show()


    def close(self):
        self.callBackUtilities.clean(force=True)
        self.window.close()

    def buildErrorWindow(self):
        window = self.QT.QScrollArea(parent = self.parentWindow)

        main_layout = self.QT.QVBoxLayout()
        headerLayout = self.QT.QHBoxLayout()
        body_layout = self.QT.QVBoxLayout()

        label = self.QT.QLabel("Select a control set and run the tool again")
        label.setAlignment(self.QTCore.Qt.AlignCenter | self.QTCore.Qt.AlignVCenter)

        headerLayout.addWidget(label)
        main_layout.addLayout(headerLayout)
        main_layout.addLayout(body_layout)

        window.setWindowTitle(EzRigCheckerEditorWindowTitle)
        window.setObjectName(EzRigCheckerEditorWindowTitle)
        window.setWidgetResizable(False)
        window.setWindowFlags(self.QTCore.Qt.Window)
        window.resize(200, 200)
        window.setLayout(main_layout)        

        return window

    def buildBaseWindow(self):
        window = self.QT.QScrollArea(parent = self.parentWindow)

        main_layout = self.QT.QVBoxLayout()        
        body_layout = self.QT.QVBoxLayout()
        headerLayout = self.QT.QHBoxLayout()

        label = self.QT.QLabel("Check Mocap Control Set")
        label.setAlignment(self.QTCore.Qt.AlignCenter | self.QTCore.Qt.AlignVCenter)
        headerLayout.setAlignment(self.QTCore.Qt.AlignTop)
        headerLayout.addWidget(label)


        resultLabelTitle = self.QT.QLabel("Result")
        resultLabelTitle.setAlignment(self.QTCore.Qt.AlignCenter | self.QTCore.Qt.AlignVCenter)
        body_layout.addWidget(resultLabelTitle)

        self.resultLabel = self.QT.QLabel("")
        self.resultLabel.setAlignment(self.QTCore.Qt.AlignCenter | self.QTCore.Qt.AlignVCenter)
        body_layout.addWidget(self.resultLabel)

        checkButton = self.QT.QPushButton()
        checkButton.setText("Check")
        checkButton.clicked.connect(lambda: self.check())
        body_layout.addWidget(checkButton)

        main_layout.addLayout(headerLayout)
        main_layout.addLayout(body_layout)

        window.setWindowTitle(EzRigCheckerEditorWindowTitle)
        window.setObjectName(EzRigCheckerEditorWindowTitle)
        window.setWidgetResizable(False)
        window.setWindowFlags(self.QTCore.Qt.Window)
        window.resize(200, 200)
        window.setLayout(main_layout)

        return window

    def check(self):
        self.errorStack = []
        self.warningStack = []

        selected = cmds.ls(sl=True)
        print cmds.objectType(cmds.ls(sl=True, st=True)[0])
        if len(cmds.ls(sl=True)) != 1:
            self.addToErrorStack("Must select exactly one objectSet!")
            self.resultLabel.setText(self.getErrorMsg())
        elif cmds.objectType(cmds.ls(sl=True, st=True)[0]) != "objectSet":
            self.addToErrorStack("Must select a objectSet!")
            self.resultLabel.setText(self.getErrorMsg())
        else:
            print "CHECKING STARTING"
            selected = cmds.ls(sl=True)         
            hierarchyObj = self.createJsonFromHierarchy(selected)

            # CON ESTO SE CREA EL ARCHIVO ORIGINAL :D.
            # json_data = json.dumps(hierarchyObj)        
            # with open(self.hierarchyTemplatePath, "w+") as text_file:
            #     text_file.write(json_data)

            compareObj = {}
            if os.path.exists(self.mocapTemplatePath):
                with open(self.mocapTemplatePath) as data_file:
                    compareObj = json.load(data_file)
                result = self.compareDict(compareObj, hierarchyObj)

                if result:
                    resultStr = "CONTROL SETS MATCH"
                else:                    
                    resultStr = "CONTRO SETS DON'T MATCH"
                    if self.hasErrors():
                        resultStr = resultStr + "\n\nErrors\n" + self.getErrorMsg()

                if self.hasWarnings():
                    resultStr = resultStr + "\nWARNINGS\n" + self.getWarningMsg()

                print resultStr
                self.resultLabel.setText(resultStr)

    def addToErrorStack(self, error, warning = False):
        if warning:
            self.warningStack.append(error)
        else:
            self.errorStack.append(error)

    def hasErrors(self):
        return len(self.errorStack) > 0

    def hasWarnings(self):
        return len(self.warningStack) > 0

    def getWarningMsg(self):
        retMsg = ""
        for msg in self.warningStack:
            retMsg = retMsg + msg + "\n"
        return retMsg

    def getErrorMsg(self):
        retMsg = ""
        for msg in self.errorStack:
            retMsg = retMsg + msg + "\n"
        return retMsg

    def createJsonFromHierarchy(self, selection):
        joint = selection[0]
        node = {}
        self.createJsonNode(joint, node)
        return node

    def createJsonNode(self, joint, prevNode):
        childNode = {}
        children = cmds.sets(joint,q=1)
        if children:
            for child in children:
                childNode[child] = {}
        prevNode[joint] = childNode

    def compareDict(self, templateDict, modelDict, previousKey = None):
        result = True
        for templateKey in templateDict.keys():
            # print "Checking template key: ", templateKey
            if templateKey not in modelDict.keys():
                # print "Key Not Found on model: ", templateKey
                self.addToErrorStack("MUST CONTROL SET: <{0}> | Parent: <{1}>".format(templateKey, previousKey))
                result = False
            else:
                # print "Entering new dict level with Key:", templateKey                
                result = result and self.compareDict(templateDict[templateKey], modelDict[templateKey], templateKey)     

        if len(templateDict) != len(modelDict):      
            # print "DIFERENCIA EN CANTIDAD DE HIJOS: ", previousKey
            # self.addToErrorStack("JOINTS AMOUNT DIFFERENCE | <{0}>".format(previousKey))
            missingKeys = [f for f in modelDict.keys() if f not in templateDict.keys()]            
            for missingKey in missingKeys:
                self.addToErrorStack("EXTRA CONTROL SET: <{0}> | Parent: <{1}>".format(missingKey, previousKey), True);

        return result

    def closeInstances(self):
        for obj in self.parentWindow.children():
            if obj.objectName() == EzRigCheckerEditorWindowTitle: # Compare object names
                obj.setParent(None)
                obj.deleteLater()  


    def setupWindow(self,main_layout):
        self.clearLayout(main_layout)

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    @staticmethod         
    def GetCurrentSelection():
        return cmds.ls(sl=True );

    @staticmethod
    def GetFullFileName():
        fullName = cmds.file(q=True,exn=True).replace(".mb","").replace(".ma","")
        return fullName

    @staticmethod
    def GetFullPath():
        fullName = os.path.dirname(cmds.file(q=True,exn=True).replace(".mb","").replace(".ma",""))+"/"
        return fullName

    @staticmethod
    def GetFileName():
        fullName = os.path.basename(cmds.file(q=True,exn=True).replace(".mb","").replace(".ma",""))
        return fullName


class EzRigCheckerEditor_MAYA(EzRigCheckerEditor):

    def __init__(self):
        super(EzRigCheckerEditor_MAYA, self).__init__()        

        selection = self.GetCurrentSelection()
        if len(selection) > 0:
            self.parentNode = selection[0]
        else:
            self.parentNode = None

        from maya import OpenMayaUI as omui 
        from PySide2 import QtGui,QtCore,QtWidgets
        from shiboken2 import wrapInstance

        self.QT = sys.modules["PySide2.QtWidgets"]
        self.QTGui = sys.modules["PySide2.QtGui"]
        self.QTCore = sys.modules["PySide2.QtCore"]

        mayaMainWindowPtr = omui.MQtUtil.mainWindow() 
        mayaMainWindow= wrapInstance(long(mayaMainWindowPtr), self.QT.QMainWindow) 

        self.parentWindow = mayaMainWindow
        self.closeInstances()
        
        if self.parentNode:
            self.errorStack = []
            self.warningStack = []

            self.mocapTemplatePath = os.path.expanduser('~/') + "MayaTemplateMocapRig.json"                 
            self.window = self.buildBaseWindow()
        else:
            self.window = self.buildErrorWindow()
    

def start():
    dataEditor = EzRigCheckerEditor_MAYA()    
    dataEditor.show()
start()