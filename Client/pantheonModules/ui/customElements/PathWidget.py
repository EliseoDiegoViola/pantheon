from pantheonModules.exporter.overrides import *
from pantheonModules.pantheonUtilities import events
import os
import re

class PathWidget(QT.QWidget):
    def __init__(self, parent=None, label=None,path=None,absolute=False,selectFolder=False):
        QT.QWidget.__init__(self, parent=parent)

        self.label = label
        self.path = path
        self.isValidPath=True
        self.isPath=True
        self.OnDataUpdate = events.EventHook()
        self.pathWidget = QT.QWidget(parent)
        self.pathWidget.setObjectName("pathWidget")
        self.selectFolder = selectFolder

        

        self.horizontalLayout_5 = QT.QHBoxLayout(self)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")

        #label
        self.labelProgram = QT.QLabel(self)
        sizePolicy = QT.QSizePolicy(QT.QSizePolicy.Minimum, QT.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelProgram.sizePolicy().hasHeightForWidth())
        self.labelProgram.setSizePolicy(sizePolicy)
        self.labelProgram.setMinimumSize(QTCore.QSize(100, 0))
        self.labelProgram.setObjectName("labelProgram")
        self.labelProgram.setText(self.label)
        self.horizontalLayout_5.addWidget(self.labelProgram)


        self.superContentPath = QT.QFrame(self)
        self.superContentPath.setFrameShape(QT.QFrame.Box)
        self.superContentPath.setFrameShadow(QT.QFrame.Plain)
        self.superContentPath.setLineWidth(2)
        self.superContentPath.setMidLineWidth(0)
        self.superContentPath.setObjectName("superContentPath")
        self.horizontalLayout_6 = QT.QHBoxLayout(self.superContentPath)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.labelPath = QT.QLineEdit(self.superContentPath)
        sizePolicy = QT.QSizePolicy(QT.QSizePolicy.Expanding, QT.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelPath.sizePolicy().hasHeightForWidth())
        self.labelPath.setSizePolicy(sizePolicy)
        font = QTGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.labelPath.setFont(font)
        self.labelPath.setObjectName("labelPath")
        self.labelPath.setText(self.path)
        self.horizontalLayout_6.addWidget(self.labelPath)
        self.horizontalLayout_5.addWidget(self.superContentPath)
        if self.path!='':
            if re.search( r'(.*):/', self.path) or re.search( r'(.*):\\', self.path):
                self.checkIsFileOrDir(self.path)
            else:
                self.isPath=False

        sizePolicy = QT.QSizePolicy(QT.QSizePolicy.Minimum, QT.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        if not absolute:
            self.changePathButton = QT.QPushButton(self.pathWidget)
            sizePolicy.setHeightForWidth(self.changePathButton.sizePolicy().hasHeightForWidth())
            self.changePathButton.setEnabled(self.isPath)
            self.changePathButton.setSizePolicy(sizePolicy)
            
            self.changePathButton.setObjectName("changePathButton")
            self.changePathButton.setText("New Path")
            self.horizontalLayout_5.addWidget(self.changePathButton)
            self.changePathButton.clicked.connect(self.openFileNameDialog)


        #self.bindEvents()    

    def openFileNameDialog(self):
        options = QT.QFileDialog.Options()
        options |= QT.QFileDialog.DontUseNativeDialog
        if self.selectFolder:
            options |= QT.QFileDialog.ShowDirsOnly
            options |= QT.QFileDialog.DontResolveSymlinks

            fileName = QT.QFileDialog.getExistingDirectory(self,"Select new Path", self.path, options=options)
        else:
            fileName, _ = QT.QFileDialog.getOpenFileName(self,"Select new Path", self.path ,"All Files (*);;Python Files (*.py)", options=options)

        if fileName:
             self.fillInputLabelPath(fileName)
             self.checkIsFileOrDir(fileName)
             self.OnDataUpdate(self)
             self.path = fileName
    

    def getPath(self):
        return self.labelPath.text()
    #def bindEvents(self):
        #if not absolute:
    def fillInputLabelPath(self,newLabel):
        self.labelPath.setText(newLabel)

    def checkIsFileOrDir(self,pathToCheck):
        if((os.path.isfile(pathToCheck)) or (os.path.isdir(pathToCheck))):
            self.labelPath.setStyleSheet('color:black;')
        else:
            self.labelPath.setStyleSheet('color:red;')
            

# C:/Projects/ElementSpace/trunk/Assets/
# F:/Projects/ArtMasters/
# ElementSpace/Artworks/ArtMasters/