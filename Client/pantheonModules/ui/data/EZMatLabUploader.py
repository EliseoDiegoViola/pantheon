import sys
import json
# import urllib2 as url
import os
import copy
import socket
# from sets import Set

from pantheonModules.exporter.overrides import *
from pantheonModules.pantheonUtilities import pantheonHelpers
from pantheonModules.pantheonUtilities import modulesLoader
from pantheonModules.conn.requests import ServerRequest
from pantheonModules.conn import serverObjects
from pantheonModules.pantheonUtilities import events
from pantheonModules.settings import *
# reload(modulesLoader)
# loader = modulesLoader.ModulesLoader()

from pantheonModules.exporter.abstraction import exportableMaterial
from pantheonModules.exporter.abstraction.exportable import EXPORTABLE_TYPE

version = 0.12
EzMatsWindowTitle = "Material Uploader " + str(version)
windowSize = {"w":500, "h":600}

class EzMaterialUploaderWindow (QT.QDialog):

    materialEditorLayout = None
    editingMaterial = None

    shadersData = {}
    shadersPropertiesWidget = None


    def __init__(self,parent,localMaterial,gameProject,serverMaterial = None):
        super(EzMaterialUploaderWindow, self).__init__(parent = parent)

        self.currentProject = gameProject
        self.shadersData = self.loadUnityMaterialsData()
        
        self.OnMaterialUploadSuccess = events.EventHook()
        self.OnMaterialUploadFail = events.EventHook()

        if isinstance(localMaterial,exportableMaterial.exportableMaterial): 
            self.localMaterial = localMaterial
        else:
            print("LocalMaterial is not an exportable material, WHAT?")

        self.serverMaterial = serverMaterial

        self.editingMaterial = localMaterial
        if localMaterial:
            self.isNew = False
        else:
            self.isNew = True
        
        self.connect(self, QTCore.SIGNAL('triggered()'), self.closeEvent)
 
    def closeEvent(self, event):
        if self.isNew:
            del(self.editingMaterial.serverMaterial)
            self.editingMaterial.serverMaterial = None
        


    def buildBaseWindow(self):
        self.setLayout(QT.QVBoxLayout())
        # dialogLayout = 

        #WINDOW CONFIG 
        sizePolicy = QT.QSizePolicy(QT.QSizePolicy.Preferred, QT.QSizePolicy.Preferred)
        self.setSizePolicy(sizePolicy)
        self.setWindowTitle(EzMatsWindowTitle)
        self.setObjectName(EzMatsWindowTitle)
        self.setMinimumSize(windowSize["w"], windowSize["h"])
        self.setWindowModality(QTCore.Qt.ApplicationModal)

        #HEADER
        headerWidget = QT.QWidget()
        headerWidget.setLayout(QT.QVBoxLayout())
        self.layout().addWidget(headerWidget)

        if not self.shadersData:
            label = QT.QLabel("THIS PROJECT {0} HAS NO SHADERS AVAIABLE ".format(str(self.currentProject)))
            label.setAlignment(QTCore.Qt.AlignCenter | QTCore.Qt.AlignVCenter)
            headerWidget.layout().addWidget(label)
            return 


        #Material Name
        label = QT.QLabel("Material : {0}".format(str(self.editingMaterial)))
        label.setAlignment(QTCore.Qt.AlignCenter | QTCore.Qt.AlignVCenter)
        headerWidget.layout().addWidget(label)

        #Shader
        shaderWidget = QT.QWidget()
        shaderWidget.setLayout(QT.QHBoxLayout())
        headerWidget.layout().addWidget(shaderWidget)

        shaderLabel = QT.QLabel("Shader : ")
        shaderLabel.setSizePolicy(QT.QSizePolicy.Minimum,QT.QSizePolicy.Minimum)
        shaderWidget.layout().addWidget(shaderLabel)

        shaderCBox = QT.QComboBox()
        shaderCBox.addItems(self.shadersData.keys())
        if self.editingMaterial.serverMaterial:
            index = shaderCBox.findText(self.editingMaterial.serverMaterial.shaderName)
            if index >= 0:
                 shaderCBox.setCurrentIndex(index)

        
        shaderCBox.currentTextChanged.connect(lambda sNiceName : self.changeMaterialShader(copy.deepcopy(self.shadersData[sNiceName].properties),self.shadersData[sNiceName].shaderName))
        shaderCBox.setSizePolicy(QT.QSizePolicy.Expanding,QT.QSizePolicy.Minimum)
        # shaderCBox.setObjectName("materialShaderCBox")
        shaderWidget.layout().addWidget(shaderCBox)

        #BODY
        scrollAreaWidget = QT.QScrollArea(self)
        scrollAreaWidget.setSizePolicy(QT.QSizePolicy(QT.QSizePolicy.MinimumExpanding , QT.QSizePolicy.MinimumExpanding ))
        scrollAreaWidget.setWidgetResizable(True)
        scrollAreaWidget.setLayout(QT.QVBoxLayout())
        self.layout().addWidget(scrollAreaWidget)

        spacer = QT.QSpacerItem(1,10,QT.QSizePolicy.Preferred,QT.QSizePolicy.Fixed)
        scrollAreaWidget.layout().addItem(spacer)

        #shader properties
        toolBox = QT.QToolBox()
        scrollAreaWidget.layout().addWidget(toolBox)

        self.shadersPropertiesWidget = QT.QWidget()
        self.shadersPropertiesWidget.setLayout(QT.QVBoxLayout())
        toolBox.addItem(self.shadersPropertiesWidget,"Properties")


        #FOOTER
        footerWidget = QT.QWidget()
        footerWidget.setLayout(QT.QHBoxLayout())
        self.layout().addWidget(footerWidget)
        
        spacer = QT.QSpacerItem(1,20,QT.QSizePolicy.Preferred,QT.QSizePolicy.Fixed)
        footerWidget.layout().addItem(spacer)   
        
        if self.serverMaterial:
            modifyButton = QT.QPushButton("MODIFY")
            modifyButton.clicked.connect(self.modifyMaterial)
            footerWidget.layout().addWidget(modifyButton)
        else:
            saveButton = QT.QPushButton("UPLOAD")
            saveButton.clicked.connect(self.uploadMaterial)
            footerWidget.layout().addWidget(saveButton)

        self.editMaterial()

        #self.changeMaterialShader(copy.deepcopy(self.shadersData["HD_Unlit"].properties),"HD_Unlit")
        

    def editMaterial(self):
        self.clearLayout(self.shadersPropertiesWidget.layout())


        properties = self.editingMaterial.getAllProperties()

        if not self.editingMaterial.serverMaterial:
            self.editingMaterial.setServerMaterial(serverObjects.GameMaterials(user=socket.gethostname()
                ,name = str(self.editingMaterial)
                ,shaderName = copy.deepcopy(self.shadersData.values()[0].shaderName)
                ,properties = copy.deepcopy(self.shadersData.values()[0].properties)
                ,project=self.currentProject
            ))
        

        textures = self.editingMaterial.getAssignedTextures()
        textures.insert(0,"None")

        for prop in self.editingMaterial.serverMaterial.properties:
            propWidget = QT.QWidget()
            propWidget.setLayout(QT.QHBoxLayout())
            
            labelName = QT.QLabel(prop.propName)
            labelName.setSizePolicy(QT.QSizePolicy.Expanding,QT.QSizePolicy.Minimum)
            labelName.setAlignment(QTCore.Qt.AlignRight | QTCore.Qt.AlignVCenter)
            propWidget.layout().addWidget(labelName)
            propType = prop.propType
            # Textures settings
            if propType == "TexEnv":
                propertiesComboBox = QT.QComboBox()
                for i in range(0,len(textures)):
                    propertiesComboBox.insertItem(i,textures[i])

                pVal = self.editingMaterial.getPropertyByname(prop.propName)
                if pVal:
                    valIndex = propertiesComboBox.findText(pVal)
                    if valIndex >= 0:
                         propertiesComboBox.setCurrentIndex(valIndex)

                propertiesComboBox.currentIndexChanged.connect(lambda index,pName = prop.propName : self.changeMaterialProperty(pName,textures[index]))
                propertiesComboBox.setSizePolicy(QT.QSizePolicy.Expanding,QT.QSizePolicy.Minimum)
                propWidget.layout().addWidget(propertiesComboBox)
            elif propType == "Color":
                pixmap_label = QT.QLabel()
                print(self.editingMaterial.getPropertyByname(prop.propName))
                colorValue = self.editingMaterial.getPropertyByname(prop.propName)
                colorsChannels = [float(p)*255 for p in colorValue[colorValue.find("(")+1:colorValue.find(")")].split(",")]
                print(" VALUES ",colorsChannels)
                pixmap = QTGui.QPixmap(100,50)
                pixmap.fill(QTGui.QColor(colorsChannels[0],colorsChannels[1],colorsChannels[2],colorsChannels[3]))
                pixmap_label.setPixmap(pixmap)
                propWidget.layout().addWidget(pixmap_label)

            self.shadersPropertiesWidget.layout().addWidget(propWidget)
        
            

    def changeMaterialShader(self,shaderProps,shaderName):
        # print shaderProps,shaderName
        self.editingMaterial.serverMaterial.properties = shaderProps
        self.editingMaterial.serverMaterial.shaderName = shaderName
        self.editMaterial()

    def changeMaterialProperty(self,prop,value):
        self.editingMaterial.editProperty(prop,value)

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    def loadUnityMaterialsData(self):
        shadersData = {}        
        #response = ServerRequest.getToolData("shaders")
        #shaders = json.loads(response.body)["shaders"]  
        searchFilter = {}  
        searchFilter["filterName"] = "project"
        searchFilter["filterValue"] = self.currentProject

        shaderFetchResponse = ServerRequest.mongoList(serverObjects.GameShaders,searchFilter)
        
        if shaderFetchResponse:
            for shader in shaderFetchResponse.objects:
                shadersData[shader.name] = shader
        # print shadersData
        return shadersData

    def uploadMaterial(self):
        try:

            print("Uploading ", str(self.editingMaterial) , " ...")


            properties = self.editingMaterial.getAllProperties()

            gameMat = self.editingMaterial.serverMaterial

            response = ServerRequest.mongoCreate(gameMat)
            if response.returnCode == 200:
                print("Everything is fine")
                self.localMaterial = self.editingMaterial
                self.OnMaterialUploadSuccess(response)
                self.close()
            else:
                print("Everything is BAD")
                self.OnMaterialUploadFail(str(response.body))
                self.close()
            

        except Exception as e:
            msg = QT.QMessageBox()
            msg.setIcon(QT.QMessageBox.Critical)
            msg.setWindowTitle("ERROR")
            msg.setText("Error on uploading")
            msg.setInformativeText("Something went wrong on uploading the " + str(self.editingMaterial))
            msg.setDetailedText(str(e))
            msg.setStandardButtons(QT.QMessageBox.Ok)
            msg.exec_()
            self.close()  

    def modifyMaterial(self):
        try:

            print("Modifying ", str(self.editingMaterial) , " ...")

            properties = self.editingMaterial.getAllProperties()

            gameMat = self.editingMaterial.serverMaterial

            response = ServerRequest.mongoUpdate(gameMat,self.serverMaterial.matData.mongoId)
            if response.returnCode == 200:
                print( "Everything is fine")
                self.OnMaterialUploadSuccess(response)
                self.close()  
            else:
                print( "Everything is BAD")
                self.OnMaterialUploadFail(str(response.body))
                self.close()

        except Exception as e:
            msg = QT.QMessageBox()
            msg.setIcon(QT.QMessageBox.Critical)
            msg.setWindowTitle("ERROR")
            msg.setText("Error on modifying")
            msg.setInformativeText("Something went wrong on modifying the " + str(self.editingMaterial))
            msg.setDetailedText(str(e))
            msg.setStandardButtons(QT.QMessageBox.Ok)
            msg.exec_()
            self.close()  

    
    # def lookMaterialsProperties(self,shaderData,shadername):
    #     for shader in shaderData:
    #         if shader["shaderName"] == shadername:
    #             return copy.deepcopy(shader["properties"])

    def closeInstances(self):
        for obj in self.parent().children():
            if obj.objectName() == EzMatsWindowTitle: # Compare object names
                obj.setParent(None)
                obj.deleteLater()        

