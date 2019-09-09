import sys

# import json
# import os
# import copy
import re
# import base64

from pantheonModules.ui.dataRepresentation.DataTextField import *
from pantheonModules.exporter.overrides import *
from pantheonModules.settings import *
#from sets import Set

from pantheonModules.ui.data.EZMatLabUploader import  EzMaterialUploaderWindow

from pantheonModules.pantheonUtilities import pantheonHelpers
from pantheonModules.pantheonUtilities import events
from pantheonModules.pantheonUtilities import fileSystemUtilities as fsu 

from pantheonModules.conn.requests import ServerRequest
from pantheonModules.conn import serverObjects

from pantheonModules.exporter.abstraction import exportableMaterial
from pantheonModules.exporter.abstraction.exportable import EXPORTABLE_TYPE
from pantheonModules.logger.ateneaLogger import AteneaLogger

from pantheonModules.exceptions.exportExceptions import CriticalExportException


version = 0.95 # version Chemistry Student
EzMatsWindowTitle = "EZMatLab " + str(version)
windowSize = {"w":800, "h":800}
materialNameChecker = "\\b(cs|fn|eb|es|gc|ko|su|gg|ms|mc|tt|me|sn|cos|in)_(foliage|fake|organic|glass|metal|concrete|wood|water|marble|stone|brick|holo|plastic|light|electronics|cloth|fabric|body|head|hair|ground|decal)_(trim|full|tile)_.*_(neat|old|cracked|rusty|moldy|dirty|base|rough)_\d\d"

class EZMaterialLibrary (QT.QMainWindow):

    def __init__(self,parent):
        super(EZMaterialLibrary, self).__init__(parent = parent)
        # ateneaLogger = loader("pantheonModules.logger.ateneaLogger")
        # self.logger = ateneaLogger.AteneaLogger()
        self.clientMaterialsWidget = None
        self.serverMaterialsWidget = None
        # self.shadersData = self.loadUnityMaterialsData()


    def eventFilter(self, source, event):
        # if (event.type() == QTCore.QEvent.FocusOut):
        #     print('eventFilter: focus out')
        if (event.type() == QTCore.QEvent.FocusIn):
            localOverride.MiscUtilities.DisableShortcuts()
            # return true here to bypass default behaviour
        # print "SEEEEELF " , self
        return super(EZMaterialLibrary, self).eventFilter(source, event)


    def closeEvent(self, event):
        localOverride.MiscUtilities.EnableShortcuts()        

    def showEvent(self, event):
        localOverride.MiscUtilities.DisableShortcuts()
   

    def buildBaseWindow(self):
        # window = QT.QScrollArea(parent = self.parentWindow)

        scrollAreaWidget = QT.QScrollArea()
        scrollAreaWidget.setSizePolicy(QT.QSizePolicy(QT.QSizePolicy.MinimumExpanding , QT.QSizePolicy.MinimumExpanding ))
        scrollAreaWidget.setWidgetResizable(True)

        windowContentWidget = QT.QWidget()
        mainContentLayout = QT.QVBoxLayout()
        windowContentWidget.setLayout(mainContentLayout)

        headerWidget = QT.QWidget()
        headerLayout = QT.QHBoxLayout()
        headerWidget.setLayout(headerLayout)

        searchBar = QT.QLineEdit() 
        searchBar.setSizePolicy(QT.QSizePolicy.Expanding, QT.QSizePolicy.Expanding)
        searchBar.textChanged.connect(self.updateFilterRegex)
        searchBar.setFocusPolicy(QTCore.Qt.StrongFocus)
        searchBar.installEventFilter(self)
        headerLayout.addWidget(searchBar)

        projectSelect = QT.QComboBox() 
        projectSelect.addItems([sp.name for sp in serverProjects.objects])
        projectSelect.currentTextChanged.connect(self.projectChanged)
        projectSelect.setSizePolicy(QT.QSizePolicy.Expanding, QT.QSizePolicy.Expanding)
        projectSelect.setFocusPolicy(QTCore.Qt.StrongFocus)
        headerLayout.addWidget(projectSelect)


        bodyWidget = QT.QWidget()
        bodyWidget.setSizePolicy(QT.QSizePolicy.Minimum, QT.QSizePolicy.MinimumExpanding)
        bodylayout = QT.QVBoxLayout()
        bodyWidget.setLayout(bodylayout)

        mainContentLayout.addWidget(bodyWidget)
        
        sizePolicy = QT.QSizePolicy(QT.QSizePolicy.Preferred, QT.QSizePolicy.Preferred)
        # sizePolicy.setHeightForWidth(True)
        self.setSizePolicy(sizePolicy)
        self.setWindowTitle(EzMatsWindowTitle)
        self.setObjectName(EzMatsWindowTitle)
        self.setMinimumSize(windowSize["w"], windowSize["h"])
        self.setCentralWidget(scrollAreaWidget)
        self.setMenuWidget(headerWidget)
        
        scrollAreaWidget.setWidget(windowContentWidget)
        

        self.setupWindow(bodyWidget)
        self.projectChanged(getCurrentProject())

    def projectChanged(self, pName):
        # print(pName)

        changeProject(pName)
        # print(pName)
        for i in range(self.serverMaterialsWidget.count()):
            item = self.serverMaterialsWidget.item(i)
            itemWidget = self.serverMaterialsWidget.itemWidget(item)

            if itemWidget.matData.project == pName:
                item.setHidden(False)
            else:
                item.setHidden(True)

    def setupWindow(self,mainWidget):
        clearLayout(mainWidget.layout())
        
        titleLayout = QT.QHBoxLayout()
        mainWidget.layout().addLayout(titleLayout)

        transferWidget = QT.QWidget()
        transferWidget.setLayout(QT.QHBoxLayout())

        mainWidget.layout().addWidget(transferWidget)

        self.serverMaterialsWidget = self.loadServerMaterials()
        transferWidget.layout().addWidget(self.serverMaterialsWidget)
        self.serverMaterialsWidget.setSizePolicy(QT.QSizePolicy.MinimumExpanding, QT.QSizePolicy.MinimumExpanding)

        self.clientMaterialsWidget = self.loadSceneMaterials()
        transferWidget.layout().addWidget(self.clientMaterialsWidget)
        self.clientMaterialsWidget.setSizePolicy(QT.QSizePolicy.MinimumExpanding, QT.QSizePolicy.MinimumExpanding)
        
        self.checkSceneMaterials()


       

    def updateFilterRegex(self,filt):
        if len(filt) > 1:
            for i in range(self.serverMaterialsWidget.count()):
                item = self.serverMaterialsWidget.item(i)
                itemWidget = self.serverMaterialsWidget.itemWidget(item)

                itemTags = itemWidget.matName.lower().split("_")
                searchTags = list(filter(lambda tag: tag and len(tag) > 1, filt.split(" ")))

                if all([st in itemTags for st in searchTags]):
                    item.setHidden(False)
                else:
                    item.setHidden(True)
        elif len(filt) == 0:
            for i in range(self.serverMaterialsWidget.count()):
                item = self.serverMaterialsWidget.item(i)
                item.setHidden(False)

            # searchPattern = filt

    def checkSceneMaterials(self):
        serverMats = self.serverMaterialsWidget.materials
        scnMats = self.clientMaterialsWidget.materials

        equalities  = [(serMat,scnMat) for serMat in serverMats for scnMat in scnMats if scnMat.matName == serMat.matName]
        
        for eqs in equalities:
            serMat = eqs[0]
            scnMat = eqs[1]
            textureMaps = scnMat.matData.getAssignedTextures()
            serverTextures = [prop.propValue for prop in serMat.matData.properties if prop.propType == "TexEnv"]

            # print scnMat.matData
            # print textureMaps
            # print serverTextures
            serverLikeLocal = all(serTex in textureMaps for serTex in serverTextures if serTex)
            localLikeServer = all(scnTex in serverTextures for scnTex in textureMaps if scnTex)
            # print all([scnTex in serverTextures and serTex in textureMaps for serTex in serverTextures for scnTex in textureMaps if serTex])

            isModified = False
            if serverLikeLocal and localLikeServer:
                isModified = False
            else:
                isModified = True

            serMat.validate(True)
            serMat.connectToSceneMaterial(scnMat)
            scnMat.validate(True,isModified)            
            # if scnMat.matName == "ms_glass_tile_fakeParallax_neat_01":
        #scnMats[0].showUploadWindow()
            # if isModified:
            #     scnMat.revertToServerMaterial()
            


    

    def createMaterial(self,serverMat):
        nodeMaterial = localOverride.MiscUtilities.CreateMaterial(serverMat.matName,serverMat.matData)
        if not nodeMaterial: 
            serverMat.validate(False)
            msg = QT.QMessageBox() #REPLACE WITH GENERIC MESSAGE BOX
            msg.setIcon(QT.QMessageBox.Warning)
            msg.setWindowTitle("Cant create material")
            msg.setText("The material " + serverMat.matName + " Cant be created")
            msg.setInformativeText("The material is most likely missing one of its textures")
            msg.setDetailedText("\n".join([prop.propValue for prop in serverMat.matData.properties if prop.propType == "TexEnv"]))
            msg.setStandardButtons(QT.QMessageBox.Ok)
            msg.exec_()
            return None

        expMat = exportableMaterial.exportableMaterial(nodeMaterial,None,EXPORTABLE_TYPE.MATERIAL)
        expMat.setServerMaterial(serverMat)
        return expMat



    def loadSceneMaterials(self):
        clientMaterialsWidget = MaterialsContainer("Scene Materials")
        clientMaterialsWidget.itemDoubleClicked.connect(lambda item : self.selectSceneMaterial(item))
       
        sceneMats = []
        allMaterials = localOverride.MiscUtilities.GetAllSceneMaterials()

        allMaterials.sort(key=lambda x: localOverride.MiscUtilities.GetObjectName(x))
        for mat in allMaterials:
            expMat = exportableMaterial.exportableMaterial(mat,None,EXPORTABLE_TYPE.MATERIAL)
            sceneMats.append(expMat)
            
        for expMaterial in sceneMats:
            matButton = ClientMaterialWidget(str(expMaterial),expMaterial)
            matButton.setSizePolicy(QT.QSizePolicy.MinimumExpanding, QT.QSizePolicy.MinimumExpanding)
            matButton.OnMaterialUploaded += self.serverMaterialUploaded
            matButton.OnMaterialModified += self.serverMaterialModified
            

            
            clientMaterialsWidget.addMaterial(matButton)

        return clientMaterialsWidget

    def loadServerMaterials(self):
        serverMaterialsWidget = MaterialsContainer("Server Materials")
        allServerMaterials = ServerRequest.mongoList(serverObjects.GameMaterials)


        for materialData in allServerMaterials.objects:
            matButton = ServerMaterialWidget(materialData.name,materialData)
            matButton.setSizePolicy(QT.QSizePolicy.MinimumExpanding, QT.QSizePolicy.MinimumExpanding)
            serverMaterialsWidget.addMaterial(matButton)
            matButton.OnChecked += lambda serverMat : self.addNewMaterial(serverMat)

        

        return serverMaterialsWidget

    def closeInstances(self,parent):
        if parent:
            for obj in parent.children():
                if obj.objectName() == EzMatsWindowTitle: # Compare object names
                    obj.setParent(None)
                    obj.deleteLater()   

# {name : "gc_decal_trim_levelDetail_neat_01"}
    def addNewMaterial(self,serverMat):
        expMat = self.createMaterial(serverMat)
        if expMat:
            scnMat = ClientMaterialWidget(serverMat.matName,expMat)
            scnMat.validate(True,False)
            serverMat.connectToSceneMaterial(scnMat)
            self.clientMaterialsWidget.addMaterial(scnMat)

    def serverMaterialUploaded(self,matData):
        matButton = ServerMaterialWidget(matData.name,matData)
        matButton.setSizePolicy(QT.QSizePolicy.MinimumExpanding, QT.QSizePolicy.MinimumExpanding)
        self.serverMaterialsWidget.addMaterial(matButton)
        matButton.OnChecked += lambda serverMat : self.addNewMaterial(serverMat)
        self.checkSceneMaterials()

    def serverMaterialModified(self,matData):
        self.checkSceneMaterials()


    def selectSceneMaterial(self,scnMaterialItem):
        scnMaterial = self.clientMaterialsWidget.itemWidget(scnMaterialItem)
        #print scnMaterial
        #print scnMaterial.matData, "selected"
        localOverride.MiscUtilities.SelectMaterial(scnMaterial.matData.objectRepresentation)
        

##### UTILS FUNCTIONS
def clearLayout(layout):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                clearLayout(item.layout())

class ErrorPopUp(QT.QWidget):
    def __init__(self):
        QT.QWidget.__init__(self)

    def paintEvent(self, e):
        dc = QPainter(self)
        dc.drawLine(0, 0, 100, 100)
        dc.drawLine(100, 0, 0, 100)            

class MaterialsContainer(QT.QListWidget):

    def __init__(self,header):
        QT.QListWidget.__init__(self,None)
        self.materials = []

    def addMaterial(self,mat):
        if isinstance(mat,MaterialWidget):
            self.materials.append(mat)

            self.addItem(mat.listItem)
            # print mat.matName
            self.setItemWidget(mat.listItem,mat)
            # mat.adjustSize()
        else:
            print("WHY!?")

class MaterialWidget(QT.QWidget):
    def __init__(self,matName,matData):
        QT.QWidget.__init__(self,None)
        self.matName = matName
        self.matData = matData
        

class ServerMaterialWidget(MaterialWidget):
    
    def __init__(self,matName,matData):
        MaterialWidget.__init__(self,matName,matData)


        # self.setSizePolicy(QT.QSizePolicy.Expanding, QT.QSizePolicy.Expanding)
        self.setLayout(QT.QHBoxLayout())
        # self.layout().addStretch(100)

        self.listItem = QT.QListWidgetItem()
        self.checkb = QT.QCheckBox()
        self.checkb.setTristate(False)
        self.checkb.setSizePolicy(QT.QSizePolicy.Minimum, QT.QSizePolicy.Minimum)
        self.checkb.stateChanged.connect(self.stateUpdated)
        # self.checkb.setFixedSize(500,500);
        self.nameLabel = QT.QLabel(matName)
        self.nameLabel.setAlignment(QTCore.Qt.AlignLeft | QTCore.Qt.AlignVCenter)
        self.nameLabel.setSizePolicy(QT.QSizePolicy.Expanding, QT.QSizePolicy.Expanding)
        # self.nameLabel.setFixedSize(500,500);
        self.previewButton = QT.QPushButton("Preview")
        self.previewButton.clicked.connect(lambda:  self.previewServerMaterial())

        self.layout().addWidget(self.checkb)
        self.layout().addWidget(self.nameLabel)
        self.layout().addWidget(self.previewButton)

        # += lambda mat : self.updateButtonStatus(mat,nameButton)+= lambda mat : self.updateButtonStatus(mat,nameButton)
        self.OnChecked = events.EventHook()
        self.OnUnChecked = events.EventHook()

        self.sceneMaterial = None

        self.listItem.setSizeHint(self.sizeHint())



    def stateUpdated(self,state):
        if state == 0:
            self.diconnectFromSceneMaterial()
            if self.OnUnChecked:
                self.OnUnChecked(self)
        elif state == 1:
            print ("TriState ERROR!?!")
        elif state == 2:
            if self.OnChecked:
                self.OnChecked(self)

    def validate(self,isValid):
        self.checkb.blockSignals(True)
        if isValid:
            self.checkb.setCheckState(QTCore.Qt.CheckState.Checked)
        else:
            self.checkb.setCheckState(QTCore.Qt.CheckState.Unchecked)
        self.checkb.blockSignals(False)  

    def connectToSceneMaterial(self,scnMat):
        if isinstance(scnMat,ClientMaterialWidget):
            print(self.matData)
            scnMat.matData.setServerMaterial(self.matData)
            self.sceneMaterial = scnMat

            scnMat.setServerMaterial(self)
        else:
            print (scnMat + " is not a ClientMaterialWidget")

    def diconnectFromSceneMaterial(self):
        if self.sceneMaterial != None:
            self.sceneMaterial.setServerMaterial(None)
            self.sceneMaterial.deleteMaterial()
            self.validate(False)
            self.sceneMaterial = None

    def previewServerMaterial(self):
        uploadWindow = PreviewWidget(self,self)
        uploadWindow.exec_()
            
class PreviewWidget(QT.QDialog):
    def __init__(self, serverMaterial , parent=None):
        QT.QDialog.__init__(self,parent=parent)
        self.serverMaterial = serverMaterial
        self.OnResized = events.EventHook()
        self.setupWindow()

    def resizeEvent(self, event):
        self.OnResized(event)
        # QtGui.QMainWindow.resizeEvent(self, event)

    def setupWindow(self):
        self.setLayout(QT.QVBoxLayout())
        # dialogLayout = 

        #WINDOW CONFIG 
        sizePolicy = QT.QSizePolicy(QT.QSizePolicy.Preferred, QT.QSizePolicy.Preferred)
        self.setSizePolicy(sizePolicy)
        self.setWindowTitle("Previewing material")
        self.setObjectName("PreviewWidget")
        self.setMinimumSize(256, 256)
        self.setWindowModality(QTCore.Qt.ApplicationModal)

        #HEADER
        headerWidget = QT.QWidget()
        headerWidget.setLayout(QT.QVBoxLayout())
        self.layout().addWidget(headerWidget)

        #Material Name
        label = QT.QLabel("Material : {0}".format(str(self.serverMaterial.matName)))
        label.setAlignment(QTCore.Qt.AlignCenter | QTCore.Qt.AlignVCenter)
        headerWidget.layout().addWidget(label)

        spacer = QT.QSpacerItem(1,10,QT.QSizePolicy.Preferred,QT.QSizePolicy.Fixed)
        self.layout().addItem(spacer)

        #BODY
        propertiesWidget = QT.QWidget()
        propertiesWidget.setSizePolicy(QT.QSizePolicy(QT.QSizePolicy.MinimumExpanding , QT.QSizePolicy.MinimumExpanding ))
        propertiesWidget.setLayout(QT.QVBoxLayout())

        propLabel = QT.QLabel()
        propLabel.setAlignment(QTCore.Qt.AlignCenter | QTCore.Qt.AlignVCenter)
        if self.serverMaterial.matData.thumbnail:
            thumbnailData = str.encode(str(self.serverMaterial.matData.thumbnail))
            byteArray = QTCore.QByteArray.fromBase64(thumbnailData);
            image = QTGui.QImage.fromData(byteArray, "PNG");
            pix = QTGui.QPixmap.fromImage(image)
            propLabel.setPixmap(pix.scaled(256,256,QTCore.Qt.KeepAspectRatio))
            self.OnResized += lambda evt : propLabel.setPixmap(pix.scaled(evt.size().width(),evt.size().height(),QTCore.Qt.KeepAspectRatio))
        else:
            propLabel.setText("Thumbnail not avaiable")

        propertiesWidget.layout().addWidget(propLabel)
        
    


        # for prop in self.serverMaterial.matData['properties']:

        #     propEntry = QT.QWidget()
        #     propEntry.setLayout(QT.QGridLayout())
        #     propertiesWidget.layout().addWidget(propEntry)

        #     propName = prop["propName"]
        #     nameLabel = QT.QLabel(propName)
        #     propEntry.layout().addWidget(nameLabel,0,0)
        #     propEntry.layout().setColumnMinimumWidth(0,150)
        #     propEntry.layout().setColumnStretch(0,0)

        #     propType = prop["propType"]
        #     typeLabel = QT.QLabel(propType)
        #     propEntry.layout().addWidget(typeLabel,0,1)
        #     propEntry.layout().setColumnMinimumWidth(1,100)
        #     propEntry.layout().setColumnStretch(1,0)

        #     propValue = prop["propValue"]

        #     propLabel = QT.QLabel()
        #     # print "new ",propLabel
        #     propEntry.layout().addWidget(propLabel,0,2)
        #     propEntry.layout().setColumnStretch(2,10)
                

        #     if propType == "TexEnv":
        #         # propLabel.setFixedWidth(200)
        #         # propLabel.setFixedHeight(200)
        #         startDir = localOverride.FileUtilities.GetFullPath()
        #         file = fsu.findFileInParents(propValue,startDir,"/Textures")
        #         if file:
        #             qim = ImageQt(file)
        #             pix = QtGui.QPixmap.fromImage(qim)

        #             # print "File found is ",file
        #             # pixmap = QTGui.QPixmap(file,"1")
        #             propLabel.setPixmap(pix.scaled(150,150))
        #             # propLabel.setText("{0} File is avaiable".format(propValue))
        #             # print "File found is ",pixmap
        #         else:
        #             # print "File Not Found"
        #             propLabel.setText("{0} File not avaiable".format(propValue))

                
        #     elif propType == "Color":
        #         propLabel= QT.QLabel()
        #         propLabel.setFixedWidth(200)
        #         propLabel.setFixedHeight(25)
        #         propLabel.setAutoFillBackground(True)

        #         colors = re.findall(r'\d+\.\d+', propValue)
        #         red = colors[0]
        #         green = colors[1]
        #         blue = colors[2]
        #         alpha = colors[3]
                
        #         values = "{r}, {g}, {b}, {a}".format(r = red,
        #                                              g = green,
        #                                              b = blue,
        #                                              a = alpha)
        #         propLabel.setStyleSheet("QLabel { background-color: rgba("+values+"); }")
        #     elif propType == "Float":
        #         propLabel= QT.QLabel()
        #         propLabel.setFixedWidth(200)
        #         propLabel.setFixedHeight(25)
        #         propLabel.setText(propValue)
        #     elif propType == "Int":
        #         propLabel= QT.QLabel()
        #         propLabel.setFixedWidth(200)
        #         propLabel.setFixedHeight(25)
        #         propLabel.setText(propValue)
        #     elif propType == "Range":
        #         propLabel= QT.QLabel()
        #         propLabel.setFixedWidth(200)
        #         propLabel.setFixedHeight(25)
        #         propLabel.setText(propValue)
        #     elif propType == "Vector":
        #         propLabel= QT.QLabel()
        #         propLabel.setFixedWidth(200)
        #         propLabel.setFixedHeight(25)
        #         propLabel.setText(propValue)
        #     else:
        #         propLabel= QT.QLabel()
        #         propLabel.setFixedWidth(200)
        #         propLabel.setFixedHeight(25)
        #         propLabel.setText(propValue)

            
        
        # propertiesWidget.setStyleSheet("border: 1px solid red");

        scrollAreaWidget = QT.QScrollArea()
        # scrollAreaWidget.setWidgetResizable(True)
        scrollAreaWidget.setStyleSheet("border: 1px solid green");
        # scrollAreaWidget.setSizePolicy(QT.QSizePolicy(QT.QSizePolicy.MinimumExpanding , QT.QSizePolicy.MinimumExpanding ))
        # scrollAreaWidget.setWidget(propertiesWidget)
        self.layout().addWidget(propertiesWidget)

class ClientMaterialWidget(MaterialWidget):

    def __init__(self,matName,scnMat):
        MaterialWidget.__init__(self,matName,scnMat)
        self.serMat = None
        self.setLayout(QT.QHBoxLayout())
        self.listItem = QT.QListWidgetItem()


        self.optWidgets = QT.QStackedWidget()
        self.optWidgets.setLayout(QT.QHBoxLayout())
        optSizePolicy = QT.QSizePolicy(QT.QSizePolicy.Minimum, QT.QSizePolicy.Minimum)
        self.optWidgets.setSizePolicy(optSizePolicy)

        uploadWidget = QT.QWidget()
        uploadWidget.setLayout(QT.QHBoxLayout())
        

        regMatch = re.match(materialNameChecker,matName,flags=re.IGNORECASE)
        if regMatch:
            uploadBtn = QT.QPushButton("Upload")        
            uploadBtn.clicked.connect(lambda:  self.showUploadWindow())
            uploadWidget.layout().addWidget(uploadBtn)
        else:
            badNameLabel = QT.QLabel("BAD NAME")
            badNameLabel.setAlignment(QTCore.Qt.AlignRight)
            uploadWidget.layout().addWidget(badNameLabel)

        
        differencesWidget = QT.QWidget()
        differencesWidget.setLayout(QT.QHBoxLayout())
        revertBtn = QT.QPushButton("Revert")
        revertBtn.clicked.connect(lambda:  self.revertToServerMaterial())
        differencesWidget.layout().addWidget(revertBtn)
        applyBtn = QT.QPushButton("Apply")
        applyBtn.clicked.connect(lambda:  self.applyChangesToServerMaterial())
        differencesWidget.layout().addWidget(applyBtn)

        syncWidget = QT.QWidget()
        syncWidget.setLayout(QT.QHBoxLayout())
        modifyBtn = QT.QPushButton("Modify")
        modifyBtn.clicked.connect(lambda:  self.applyChangesToServerMaterial())
        syncWidget.layout().addWidget(modifyBtn)
        # self.showUploadWindow()

        self.optWidgets.insertWidget(0,uploadWidget)
        self.optWidgets.insertWidget(1,differencesWidget)
        self.optWidgets.insertWidget(2,syncWidget)

        # self.checkb.stateChanged.connect(self.stateUpdated)
        self.nameLabel = QT.QLabel(matName)
        self.nameLabel.setAlignment(QTCore.Qt.AlignRight | QTCore.Qt.AlignVCenter)

        self.layout().addWidget(self.nameLabel)
        self.layout().addWidget(self.optWidgets)

        self.OnMaterialUploaded = events.EventHook()
        self.OnMaterialModified = events.EventHook()
        self.OnMaterialReverted = events.EventHook()

        # self.listItem.setSizeHint(QTCore.QSize(200,20))
        self.listItem.setSizeHint(self.sizeHint())
        
        self.validate(False,False)

    def showUploadWindow(self):
        #FIX ON CANCEL
        print(getCurrentProject())
        # self.matData.setServerMaterial(GameMaterials(user="temp"
        #     ,name=str(self.matData)
        #     ,shaderName=None
        #     ,properties=[]
        #     ,project="temp"
        # ))
        uploadWindow = EzMaterialUploaderWindow(self,self.matData,getCurrentProject())
        uploadWindow.closeInstances() 
        uploadWindow.buildBaseWindow()
        uploadWindow.OnMaterialUploadSuccess += self.scnMaterialUploaded
        uploadWindow.OnMaterialUploadFail += lambda failMessage : self.showPopUp("Upload Failed","{0} cant be uploaded".format(str(self.matName)),"",failMessage)
        uploadWindow.exec_()

    def applyChangesToServerMaterial(self):
        uploadWindow = EzMaterialUploaderWindow(self,self.matData,getCurrentProject(),self.serMat)
        uploadWindow.closeInstances() 
        uploadWindow.buildBaseWindow()
        uploadWindow.OnMaterialUploadSuccess += self.scnMaterialModified
        uploadWindow.OnMaterialUploadFail += lambda failMessage : self.showPopUp("Apply Failed","{0} cant be Modified, call a programmer".format(str(self.matName)),"",failMessage)
        uploadWindow.exec_()


    def scnMaterialUploaded(self,serverResponse):
        print(serverResponse)
        self.OnMaterialUploaded(serverResponse.objects[0])

    def scnMaterialModified(self,serverResponse):
        print(serverResponse)
        self.OnMaterialModified(serverResponse.objects[0])

    def showPopUp(self,title,message,information,details):
        msg = QT.QMessageBox()
        msg.setIcon(QT.QMessageBox.Warning)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setInformativeText(information)
        msg.setDetailedText(details)
        msg.setStandardButtons(QT.QMessageBox.Ok)
        msg.exec_()

    def revertToServerMaterial(self):
        if self.serMat:
            self.matData.setServerMaterial(self.serMat.matData)
            materialReseted = localOverride.MiscUtilities.ResetMaterial(self.matData.objectRepresentation,self.serMat.matData)
            if materialReseted:
                self.validate(True,False)
                self.OnMaterialReverted(self)
            else:
                msg = QT.QMessageBox() #REPLACE WITH GENERIC MESSAGE BOX
                msg.setIcon(QT.QMessageBox.Warning)
                msg.setWindowTitle("Cannot revert material")
                msg.setText("The material " + self.matName + " Cant be resseted")
                msg.setInformativeText("The material is most likely missing one of its textures")
                msg.setDetailedText("\n".join([prop.propValue for prop in self.serMat.matData.properties if prop.propType == "TexEnv"]))
                msg.setStandardButtons(QT.QMessageBox.Ok)
                msg.exec_()
        else:
            print("Cannot revert without server material")
        

    def validate(self,isValid,isModified):
        if isValid:
            if isModified:
                self.optWidgets.setCurrentIndex(1)
                self.nameLabel.setStyleSheet('QLabel {color: yellow;}')
            else:
                self.optWidgets.setCurrentIndex(2)
                self.nameLabel.setStyleSheet('QLabel {color: lime;}')                
        else:
            self.optWidgets.setCurrentIndex(0)
            self.nameLabel.setStyleSheet('QLabel {color: Red;}')

    def setServerMaterial(self,serMat):
        self.serMat = serMat 

    def deleteMaterial(self):
        wList = self.listItem.listWidget()
        wList.takeItem(wList.row(self.listItem))
        clearLayout(self.layout())
        self.matData.deleteMaterial()
        self.deleteLater()
        # self.listItem.deleteLater()