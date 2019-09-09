try:
    set
except NameError: 
    from sets import Set as set

from pantheonModules.exporter.overrides import *
from pantheonModules.conn import *
from pantheonModules.ui.data import *

from pantheonModules.pantheonUtilities import pantheonHelpers
from pantheonModules.logger.ateneaLogger import AteneaLogger
EzDataEditorWindowTitle = "EzDataEditor 1.45" # Version : PAN

class EzDataEditor(QT.QMainWindow):

    types = None
    subtypes = None
    dataNames = None
    dataTypes = None


    def __init__(self,dataContainer,parent =  None):
        super(EzDataEditor, self).__init__(parent = parent)
        self.avaibleData = ["ObjectExtraData"]
        self.dataContainer = dataContainer
        self.types = serverData["ezData"]["objectTypes"]
        self.subtypes = serverData["ezData"]["objectSubTypes"]
        self.dataNames = serverData["ezData"]["dataNames"]
        self.dataTypes = serverData["ezData"]["dataTypes"]
        self.installEventFilter(self)
    
    def eventFilter(self, source, event):
        
        if (event.type() == QTCore.QEvent.Type.Enter):
            localOverride.MiscUtilities.DisableShortcuts()
        if (event.type() == QTCore.QEvent.Type.Leave):
            localOverride.MiscUtilities.EnableShortcuts()
        return super(EzDataEditor, self).eventFilter(source, event)




    def closeEvent(self, event):
        localOverride.MiscUtilities.EnableShortcuts()        

    def showEvent(self, event):
        localOverride.MiscUtilities.DisableShortcuts()



    # def show(self):
    #     # print (self.window)
    #     localOverride.MiscUtilities.DisableShortcuts()
    #     self.window.show()



    # def close(self):
    #     # self.callBackUtilities.clean(force=True)
    #     localOverride.MiscUtilities.EnableShortcuts()
    #     self.window.close()

    def updateValues(self, ezField):
        data = ezField.saveObject()
        extraData = localOverride.DataParser.nodeAttribute(ParentNode,self.dataContainer)
        extraData.editCustomParameter(ezField.dataName,data,localOverride.DataParser.nodeAttribute.ATTR_TYPES.STRING)


    def drawElement(self):
        layout = QT.QHBoxLayout()

        deleteButton.setText("X")
        deleteButton.setMaximumWidth(dField.deleteButton.fontMetrics().boundingRect("X").width() + 7)
        deleteButton.clicked.connect(lambda:  self.deleteData(dField))
        layout.addWidget(deleteButton)

        
        return layout

    def createParamter(self,container,paramName,paramType,paramDefaultValue,new = False):        
        print ("Type ",paramType)
        print ("Value ",paramDefaultValue)

        if new:
            extraData = localOverride.DataParser.nodeAttribute(ParentNode,self.dataContainer)
            dataName = extraData.addCustomParameter(paramName,"",localOverride.DataParser.nodeAttribute.ATTR_TYPES.STRING)
            if not dataName:
                return None

        valueField = EZDataObject(dataName = paramName, dataType = paramType, dataValue =paramDefaultValue, parent = container)
        valueField.OnObjectRemoved += self.deleteData
        valueField.OnDataUpdate += lambda innerField : self.updateValues(valueField) 
        
        container.layout().addWidget(valueField)
        return valueField


    def addNewParameter(self,container,paramName,paramType,paramDefaultValue):
        newValueField = self.createParamter(container,paramName,paramType,paramDefaultValue,new = True)
        self.updateValues(newValueField) # SAVE DEFAULT DATA
        return newValueField

        
            

    def deleteData(self,dField):
        extraData = localOverride.DataParser.nodeAttribute(ParentNode,self.dataContainer)
        extraData.deleteCustomParameter(dField.dataName)

    def setupErrorWindow(self):
        main_widget = QT.QWidget()
        main_layout = QT.QVBoxLayout()
        main_widget.setLayout(main_layout)

        headerLayout = QT.QHBoxLayout()
        body_layout = QT.QVBoxLayout()

        label = QT.QLabel("Select a parent and run the tool again")
        label.setAlignment(QTCore.Qt.AlignCenter | QTCore.Qt.AlignVCenter)

        headerLayout.addWidget(label)
        main_layout.addLayout(headerLayout)
        main_layout.addLayout(body_layout)



        self.setWindowTitle(EzDataEditorWindowTitle)
        self.setObjectName(EzDataEditorWindowTitle)
        self.setFixedSize(600, 600)
        self.setCentralWidget(main_widget)

    def setupBaseWindow(self,dataIndex):
        self.dataContainer = self.avaibleData[dataIndex]

        self.paramNameCBox = QT.QComboBox() ##KIND... OF... HACK!

        scrollAreaWidget = QT.QScrollArea()
        scrollAreaWidget.setSizePolicy(QT.QSizePolicy(QT.QSizePolicy.MinimumExpanding , QT.QSizePolicy.MinimumExpanding ))
        scrollAreaWidget.setWidgetResizable(True)

        # windowLayout = QT.QVBoxLayout()
        windowContentWidget = QT.QWidget()
        main_layout = QT.QVBoxLayout()

        headerWidget = QT.QWidget()
        headerLayout = QT.QVBoxLayout()
        headerWidget.setLayout(headerLayout)

        bodyWidget = QT.QWidget()
        bodyWidget.setSizePolicy(QT.QSizePolicy.Minimum, QT.QSizePolicy.Minimum)
        bodylayout = QT.QVBoxLayout()
        bodyWidget.setLayout(bodylayout)

        criticalDataFrame = QT.QFrame()
        criticalDataLayout = QT.QVBoxLayout()

        typeLayout = QT.QHBoxLayout()
        subtypeLayout = QT.QHBoxLayout()

        labelType = QT.QLabel("TYPE : ")
        typesCBox = QT.QComboBox()

        labelSType = QT.QLabel("SUB TYPE : ")
        subtCBox = QT.QComboBox()

        typeLayout.addWidget(labelType)
        typeLayout.addWidget(typesCBox)
        subtypeLayout.addWidget(labelSType)
        subtypeLayout.addWidget(subtCBox)

        baseData = localOverride.DataParser.nodeAttribute(ParentNode,"ObjectBaseData")

        currentTyp = baseData.getCustomParameter("type")
        currentSTyp = baseData.getCustomParameter("subtype")

        if currentTyp == None:
            currentTyp = self.types[0]
            baseData.addCustomParameter("type",currentTyp)
        else:
            currentTyp = currentTyp.parameterValue

        for i in range(0,len(self.types)):
            typesCBox.insertItem(i,self.types[i])
            if self.types[i] == currentTyp:
                typesCBox.setCurrentIndex(i)

        typesCBox.currentIndexChanged.connect(lambda index : self.updateType(self.types[index],subtCBox))
        subtCBox.currentIndexChanged.connect(lambda index : self.updateSubType(self.subtypes[self.types[typesCBox.currentIndex()]][index],self.types[typesCBox.currentIndex()]))
        
        self.updateType(currentTyp,subtCBox)


        criticalDataLayout.addLayout(typeLayout)
        criticalDataLayout.addLayout(subtypeLayout)
        criticalDataFrame.setLineWidth(2);
        criticalDataFrame.setFrameStyle(QT.QFrame.Panel | QT.QFrame.Raised);
        criticalDataFrame.setSizePolicy(QT.QSizePolicy.Minimum, QT.QSizePolicy.Minimum)

        criticalDataFrame.setLayout(criticalDataLayout)

        headerLayout.addWidget(criticalDataFrame)

        # main_layout.addWidget(headerWidget)
        main_layout.addWidget(bodyWidget)
        main_layout.setAlignment(QTCore.Qt.AlignTop)



        sizePolicy = QT.QSizePolicy(QT.QSizePolicy.Preferred, QT.QSizePolicy.Preferred)
        sizePolicy.setHeightForWidth(True)
        self.setSizePolicy(sizePolicy)
        self.setWindowTitle(EzDataEditorWindowTitle)
        self.setObjectName(EzDataEditorWindowTitle)
        self.setMinimumSize(800,600)
        self.setCentralWidget(scrollAreaWidget)
        self.setMenuWidget(headerWidget)
        
        scrollAreaWidget.setWidget(windowContentWidget)
        windowContentWidget.setLayout(main_layout)

        self.setupWindow(bodyWidget)


        # window.resize(800, 600)
        # print bodyWidget.resize(1800,800)        

        # return window

    def updateType(self,newType,subtCBox):
        baseData = localOverride.DataParser.nodeAttribute(ParentNode,"ObjectBaseData")
        currentSTyp = baseData.getCustomParameter("subtype")

        subtCBox.clear() 
        if newType != "None":
            for i in range(0,len(self.subtypes[newType])):
                subtCBox.insertItem(i,self.subtypes[newType][i])
                if currentSTyp and self.subtypes[newType][i] == currentSTyp.parameterValue:
                    subtCBox.setCurrentIndex(i)

        baseData.editCustomParameter("type",newType)

        
        if currentSTyp == None or currentSTyp.parameterValue not in self.dataNames[self.dataContainer][newType]:
            baseData.addCustomParameter("subtype","None")
            self.updateSubType(self.subtypes[newType][0],newType)
        else:
            self.updateSubType(currentSTyp.parameterValue,newType)
        

    def updateSubType(self,newSType,newType):
        baseData = localOverride.DataParser.nodeAttribute(ParentNode,"ObjectBaseData")
        baseData.editCustomParameter("subtype",newSType)


        self.paramNameCBox.clear()
        for key in self.dataNames[self.dataContainer][newType][newSType]:
            userData = self.dataNames[self.dataContainer][newType][newSType][key]
            userData["varName"] = key
            self.paramNameCBox.insertItem(
                self.paramNameCBox.count() ,
                key,
                userData = userData)
        
    

    def closeInstances(self,parent):
        if parent:
            for obj in parent.children():
                if obj.objectName() == EzDataEditorWindowTitle: # Compare object names
                    obj.setParent(None)
                    obj.deleteLater()        



    def setupWindow(self,mainDataWidget):
        clearLayout(mainDataWidget.layout())

        dataWidget = QT.QWidget()
        dataWidget.setSizePolicy(QT.QSizePolicy.Expanding, QT.QSizePolicy.Minimum)
        dataLayout = QT.QVBoxLayout()
        dataWidget.setLayout(dataLayout)

        

        baseData = localOverride.DataParser.nodeAttribute(ParentNode,"ObjectBaseData")

        extraData = localOverride.DataParser.nodeAttribute(ParentNode,self.dataContainer)
        extraParameters = extraData.listCustomParametersNames()

        currentTyp = baseData.getCustomParameter("type")
        currentSTyp = baseData.getCustomParameter("subtype")

        for parameter in extraParameters:
            extraParameter = extraData.getCustomParameter(parameter)
            self.paramNameCBox.itemData (self.paramNameCBox.currentIndex())

            print(extraParameter.parameterName)
            print(self.dataNames[self.dataContainer][currentTyp.parameterValue][currentSTyp.parameterValue])

            paramType = self.dataNames[self.dataContainer][currentTyp.parameterValue][currentSTyp.parameterValue][extraParameter.parameterName]["varType"]
            paramDefault = self.dataNames[self.dataContainer][currentTyp.parameterValue][currentSTyp.parameterValue][extraParameter.parameterName]["varDefault"]
            uiParameter = self.createParamter(container = dataWidget,
                paramName = extraParameter.parameterName,
                paramType = paramType,
                paramDefaultValue = paramDefault)
            
            uiParameter.OnDataUpdate.muteCalls(True)

            uiParameter.loadObject(extraParameter.parameterValue)

            uiParameter.OnDataUpdate.muteCalls(False)

        #FOOTER
        footerWidget = QT.QFrame()
        footerWidget.setLineWidth(2);
        footerWidget.setFrameStyle(QT.QFrame.Panel | QT.QFrame.Raised);
        footerLayout = QT.QVBoxLayout()
        footerWidget.setLayout(footerLayout)
        

        titleWidget = QT.QWidget()
        titleLayout = QT.QHBoxLayout()
        titleWidget.setLayout(titleLayout)     
        label = QT.QLabel("Data Name")
        label.setAlignment(QTCore.Qt.AlignCenter | QTCore.Qt.AlignVCenter)
        titleLayout.addWidget(label)


        label = QT.QLabel("Data Value")
        label.setAlignment(QTCore.Qt.AlignCenter | QTCore.Qt.AlignVCenter)
        titleLayout.addWidget(label)
        footerWidget.layout().addWidget(titleWidget)

        #BUTTONS
        addButton = QT.QPushButton("ADD")

        addButton.clicked.connect(lambda :
            self.addNewParameter(container = dataWidget,
                paramName = self.paramNameCBox.itemData (self.paramNameCBox.currentIndex())["varName"],
                paramType = self.paramNameCBox.itemData (self.paramNameCBox.currentIndex())["varType"],
                paramDefaultValue = self.paramNameCBox.itemData (self.paramNameCBox.currentIndex())["varDefault"]
                )
            ########### RETROCOMPATIBILITY ###########
            # if self.paramNameCBox.itemData (self.paramNameCBox.currentIndex())["varName"] != "objectAnimations" else
            #     self.addNewParameter(container = dataWidget,
            #     paramName = self.paramNameCBox.itemData (self.paramNameCBox.currentIndex())["varName"],
            #     paramType = self.paramNameCBox.itemData (self.paramNameCBox.currentIndex())["varType"],
            #     paramDefaultValue = self.paramNameCBox.itemData (self.paramNameCBox.currentIndex())["varDefault"]
            #     ).tryToLoadJsonAnim()
            ########### RETROCOMPATIBILITY ###########
            )
        buttonlayout = QT.QHBoxLayout() 
        buttonWidget = QT.QWidget()
        buttonlayout.addWidget(self.paramNameCBox)
        buttonlayout.addWidget(addButton)
        buttonWidget.setLayout(buttonlayout)
        footerWidget.layout().addWidget(buttonWidget)
        
        mainDataWidget.layout().addWidget(footerWidget)
        mainDataWidget.layout().addWidget(dataWidget)



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

