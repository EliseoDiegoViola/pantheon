import sys
import os
from PyQt5 import QtGui,QtCore,QtWidgets,uic,Qt
from PyQt5.QtWidgets import QApplication,QWidget, QInputDialog, QLineEdit, QFileDialog, QPushButton, QAction, QLineEdit, QMessageBox,QLabel,QHBoxLayout,QVBoxLayout
from enum import Enum
import UI.resources.icons.icons
import UI.resources.fileStatuses.fileStatuses
import UI.resources.statuses.statuses

import json
from UI.windows.mainWindow.addProject import *
from pantheonModules.ui.customElements.PathWidget import *
from pantheonModules.pantheonUtilities import events , fileSystemUtilities as fsu , iniConfig


import glob




class CreateProjectPopUp(QtWidgets.QDialog):
    settings = [("projectPath",False,True),("artMasterPath",False,True),("engineExport",True,True)]

    def __init__(self):
        super().__init__()
        self.settingsWidget = []
        self.createWindow = Ui_createNewProjectDialog()
        self.setWindowFlags(QtCore.Qt.Dialog)
        self.createWindow.setupUi(self)
        self.addSettings()
        self.projectCreated = events.EventHook()
        self.createWindow.saveButton.clicked.connect(self.save)

    def addSettings(self):
        for setting in CreateProjectPopUp.settings:
            add = PathWidget(self.createWindow.settingsContainer,setting[0],"",setting[1],setting[2])
            self.settingsWidget.append(add)
            self.createWindow.settingsContainer.layout().addWidget(add)

    def save(self):
        path = os.getenv('APPDATA')+"\\Pantheon\\"
        projectContent = {}

        projectContent["paths"] = {}
        for settting in self.settingsWidget:
            if settting.getPath():
                projectContent["paths"][settting.label] = settting.getPath()
            else:
                print("Fill all fields!")
                return

        projectName = self.createWindow.projectNameInput.text().lower()
        projectContent["projectName"] = projectName
        if not projectName:
            print("Need a project name!")
            return

        self.createProjectFile(projectContent,path+projectName+".atnp")
        self.projectCreated(path)
        self.done(0)

    def createProjectFile(self,settings,path):
        
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))

        file = open(path,'w')
        file.write(json.dumps(settings))
        file.close()
