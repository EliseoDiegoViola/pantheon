from pantheonModules.exporter.overrides import *
from pantheonModules.conn import *
from pantheonModules.ui.dataRepresentation.DataCheckBox import *
from pantheonModules.ui.dataRepresentation.DataComboBox import *
from pantheonModules.ui.dataRepresentation.DataTextField import *
from pantheonModules.ui.customElements.CollapsibleWidget import *
from pantheonModules.pantheonUtilities import events

try:
  basestring
except NameError:
  basestring = str
import re


class EZDataObject(QT.QFrame):

    def __repr__(self):
        return self.dataName

    def __init__(self,parent = None, dataName = "",dataType = "",dataValue = []):
        QT.QFrame.__init__(self,parent)
        dataTypes = serverData["ezData"]["dataTypes"]

        self.dataField = None
        self.dataType = dataType
        self.dataName = dataName
        self.OnDataUpdate = events.EventHook()
        self.OnObjectRemoved = events.EventHook()
        self.dataParent = parent



        typeMatch = re.findall("(^\w+)|((?<=<).*(?=>))",dataType) # Detect generic types

        if typeMatch and len(typeMatch) == 1:
            self.dataField = []
            if dataType in dataTypes:  # is a data defined data type
                dataType = dataTypes[dataType]
                for fields in dataType:
                    varName = fields["fieldName"]
                    varType = fields["fieldType"]
                    varValue = fields["fieldValue"]
                    dataField = EZDataObject(dataName=varName,dataType=varType,dataValue=varValue,parent = self )
                    dataField.OnDataUpdate += self.OnDataUpdate
                    self.dataField.append(dataField)
            else: # Is a built-in data type
                # try:
                self.dataField = eval(dataType+"()")
                self.dataField.drawElement().setParent(self) #Mmmmhhh
                self.dataField.setName(dataName)
                self.dataField.OnDataUpdate += self.OnDataUpdate
                valueParameter = []

                for dValue in dataValue:
                    if isinstance(dValue, basestring): 
                        valueMatch = re.findall("^(\w+)(?=\((.*)\))",dValue) #detect functions 

                        if valueMatch:
                            function = valueMatch[0][0]
                            parameters = valueMatch[0][1].split(",")
                            for param in parameters:
                                pass
                            parsedValue = eval(function+"()")
                            valueParameter.append(parsedValue)
                        else:
                            valueParameter.append(dValue)
                    else:
                        valueParameter.append(dValue)
                
                self.dataField.setValue(*valueParameter)
                    
                # except NameError as se:
                #     raise Exception("Trying to create invalid data {0} for {1}".format(dataName,dataType))
                    
        elif typeMatch and len(typeMatch) == 2: # is a generic data structure
            dataType = typeMatch[0][0]
            genericType = typeMatch[1][1]

            valueParameter = []

            for dValue in dataValue:
                if isinstance(dValue, basestring): 
                    valueMatch = re.findall("^(\w+)(?=\((.*)\))",dValue) #detect functions 

                    if valueMatch:
                        function = valueMatch[0][0]
                        parameters = valueMatch[0][1].split(",")
                        for param in parameters:
                            pass
                        parsedValue = eval(function+"()")
                        valueParameter.append(parsedValue)
                    else:
                        valueParameter.append(dValue)
                else:
                    valueParameter.append(dValue)
            
            # self.dataField.setValue(*valueParameter)

            self.dataField = eval("EZData{0}".format(dataType))(dataName="items",dataType=genericType,dataValue=valueParameter,parent = self)
            # self.dataField = EZDataArray("items",genericType,dataValue,parent = self)
            self.dataField.OnDataUpdate += self.OnDataUpdate

        else:
            raise Exception("Data Type error in {0} for type {1}".format(self.dataName,self.generic))



        self.buildLayout()


    def objectRemoved(self):
        self.OnObjectRemoved(self)
        self.deleteLater()
        # print self.dataParent
        if isinstance(self.dataParent,EZDataObject) or isinstance(self.dataParent,EZDataArray) or isinstance(self.dataParent,EZDataTree) or isinstance(self.dataParent,DataBase) :
            self.dataParent.OnDataUpdate(self)

        



    def loadObject(self,data):
        # print "DATA IS ",data
        if isinstance(self.dataField, list): # Im an Object
            for dataF in self.dataField:
                if dataF.dataName in data:
                    dataF.loadObject(data[dataF.dataName])
        elif isinstance(self.dataField, EZDataArray): #Im an Array TODO: Move this thing inside EZDataArray.loadObject 
            for itemData in data:
                item = self.dataField.addItem()
                item.loadObject(itemData)
        elif isinstance(self.dataField, EZDataTree): #Im an Tree
            self.dataField.loadObject(data)
        elif isinstance(self.dataField,  DataBase): #Im a field
            self.dataField.OnDataUpdate.muteCalls(True)
            self.dataField.setValue(data)
            self.dataField.OnDataUpdate.muteCalls(False)

    def saveObject(self):
        if isinstance(self.dataField, list): # Im an Object
            objectData = {}
            for dataF in self.dataField:
                objectData[dataF.dataName] = dataF.saveObject()
            return objectData
        elif isinstance(self.dataField, EZDataArray) or isinstance(self.dataField, EZDataTree): #Im an Array or a Tree
            return self.dataField.saveObject()
        elif isinstance(self.dataField,  DataBase): #Im a field
            return self.dataField.getValue()


    def buildLayout(self):
        main_layout = QT.QHBoxLayout()

        if isinstance(self.dataField, list): # Im an Object
            fieldsContainer = CollapsibleWidget(title=self.dataName)
            main_layout.addWidget(fieldsContainer)
            for element in self.dataField:
                fieldsContainer.addWidget(element)
            fieldsContainer.setLineWidth(3)
            fieldsContainer.setFrameStyle(QT.QFrame.Panel | QT.QFrame.Raised)

        elif isinstance(self.dataField, EZDataArray) or isinstance(self.dataField,  EZDataTree): #Im an Array or Tree
            nameLabel = QT.QLabel()
            nameLabel.setText(self.dataName + " : ")
            nameLabel.setSizePolicy(QT.QSizePolicy.Minimum, QT.QSizePolicy.Minimum)
            self.dataField.setSizePolicy(QT.QSizePolicy.Expanding, QT.QSizePolicy.Preferred)
            main_layout.setAlignment(QTCore.Qt.AlignLeft)
            main_layout.addWidget(nameLabel)
            fieldsContainer = QT.QWidget()
            fieldsLayout = QT.QVBoxLayout()
            fieldsContainer.setLayout(fieldsLayout)
            main_layout.addWidget(fieldsContainer)
            fieldsLayout.addWidget(self.dataField)

        elif isinstance(self.dataField,  DataBase): #Im a field

            if not isinstance(self.dataParent, EZDataTree):
                nameLabel = QT.QLabel()
                nameLabel.setText(self.dataName + " : ")
                nameLabel.setSizePolicy(QT.QSizePolicy.Minimum, QT.QSizePolicy.Minimum)
                main_layout.addWidget(nameLabel)
            
            main_layout.setAlignment(QTCore.Qt.AlignLeft)
            fieldsContainer = QT.QWidget()
            fieldsLayout = QT.QVBoxLayout()
            fieldsContainer.setLayout(fieldsLayout)
            main_layout.addWidget(fieldsContainer)
            fieldsLayout.addWidget(self.dataField.drawElement())

        if isinstance(self.dataParent, EZDataArray) or (not isinstance(self.dataParent, EZDataObject) and not isinstance(self.dataParent, EZDataTree)):
            deleteButton = QT.QPushButton()
            deleteButton.setText("X")
            deleteButton.setMaximumWidth(deleteButton.fontMetrics().boundingRect("X").width() + 7)
            deleteButton.clicked.connect(lambda :  self.objectRemoved())
            main_layout.addWidget(deleteButton)

        self.setLayout(main_layout)

###################### RETROCOMPATIBILITY ######################
    def tryToLoadJsonAnim(self):
        dataParser = localOverride.DataParser(localOverride.FileUtilities.GetFullFileName())
        allAnimations = dataParser.anims
        allEvents = dataParser.events
        allExportableAnim = []
        for anim in allAnimations:
            expAnim = {}
            expAnim["clipName"] = anim["clipName"]
            expAnim["startFrame"] = anim["clipStart"]
            expAnim["endFrame"] = anim["clipEnd"]
            expAnim["isLoop"] = bool(anim["clipLoop"])
            expAnim["isRoot"] = bool(anim["clipRoot"])

            animEvents = []
            for evnt in allEvents:
                if anim["clipStart"] <= evnt["clipKeyFrame"] <= anim["clipEnd"]: #CHECK UNTIL the eze anim allows to define events per animation
                    expEvnt = {} 
                    expEvnt["keyFrame"] = evnt["clipKeyFrame"]
                    expEvnt["eventName"] = evnt["clipKeyEvent"]
                    animEvents.append(expEvnt)

            expAnim["events"] = animEvents
            allExportableAnim.append(expAnim)
        self.loadObject(allExportableAnim)

###################### RETROCOMPATIBILITY ######################

        
class EZDataArray(QT.QFrame):


    def __init__(self,parent = None ,dataName = "" ,dataType = "",dataValue = []):
        QT.QFrame.__init__(self,parent)
        dataTypes = serverData["ezData"]["dataTypes"]
        self.items = []
        self.generic = dataType
        self.dataName = dataName
        self.OnDataUpdate = events.EventHook()
        self.dataParent = parent
        self.fieldsContainer = None
        self.setAcceptDrops(True)

        self.buildLayout()


    def loadObject(self,data):
        pass

    def saveObject(self):
        data = []
        for item in self.items:
            data.append(item.saveObject())
        return data

    def addItem(self):
        valueField = EZDataObject(dataName = "item ",dataType = self.generic,parent = self)
        valueField.OnObjectRemoved += self.removeItem
        valueField.OnDataUpdate += self.OnDataUpdate
        self.fieldsContainer.addWidget(valueField)
        self.items.append(valueField)
        self.OnDataUpdate(self)
        return valueField

    def removeItem(self,item):
        self.items.remove(item)

    def buildLayout(self):
        main_layout = QT.QHBoxLayout()

        self.fieldsContainer = CollapsibleWidget(title=self.dataName)
        main_layout.addWidget(self.fieldsContainer)
        self.fieldsContainer.setLineWidth(3)
        self.fieldsContainer.setFrameStyle(QT.QFrame.Panel | QT.QFrame.Raised)

        addButton = QT.QPushButton("Add")
        addButton.clicked.connect(self.addItem)
        self.fieldsContainer.addWidget(addButton)
        # self.addItem()
        

        self.setLayout(main_layout)

    def dragEnterEvent(self, e):

        if 'application/x-qt-windows-mime;value="DevExpress.XtraTreeList.Nodes.TreeListNode"' in e.mimeData().formats(): #Nodo del inspector
            e.accept()
        else:
            e.ignore()
            
    def dropEvent(self, e):
        selection = localOverride.MiscUtilities.GetCurrentSelection()
        if len(selection) > 0 :
            for sel in selection:
                nodeName =  localOverride.MiscUtilities.GetObjectName(sel)

                self.OnDataUpdate.muteCalls(True)
                item = self.addItem() 
                if isinstance(item.dataField,list):
                    for df in item.dataField:
                        if isinstance(df.dataField,  DataBase) and "node" in df.dataName : 
                            df.dataField.setValue(nodeName) 
                self.OnDataUpdate.muteCalls(False)

                self.OnDataUpdate(self)
        else:
            "Nothing selected?"

class EZDataTree(QT.QFrame):


    def __init__(self,parent = None,dataName = "",dataType = "",dataValue = []):
        QT.QFrame.__init__(self,parent)
        print ("AAAAA" , dataValue)
        if len(dataValue) != 1 : raise Exception("Cant create TREE with multiple list values {0}".format(dataValue))

        dataTypes = serverData["ezData"]["dataTypes"]
        # self.items = []
        self.generic = dataType
        self.dataName = dataName
        self.OnDataUpdate = events.EventHook()
        self.dataParent = parent
        self.treelist = dataValue[0]
        self.fieldsContainer = None
        self.treeWidget = None # FIXME : Delete this reference, clean the code
        # self.setAcceptDrops(True)


        self.buildLayout()


    def loadObject(self,data):
        if data:
            for itemData in data:
                
                treeItem = next(iter(self.treeWidget.findItems(itemData["node"], QTCore.Qt.MatchExactly | QTCore.Qt.MatchRecursive, 0)),None)
                
                if not treeItem:
                    print("{0} was not found , cleaning node".format(itemData["node"]) )
                    continue

                

                itemDataList = list(itemData) 
                for itemDataKey in itemDataList:

                    dataItem = itemData[itemDataKey]

                    #Maybe this should be cached?
                    headerIndex = next(iter([columnIndex for columnIndex in range(self.treeWidget.headerItem().columnCount()) if self.treeWidget.headerItem().text(columnIndex) == itemDataKey]),None)

                    if headerIndex:
                        treeItem.widgetsUpdated[headerIndex] = True

                        dataWidget = self.treeWidget.itemWidget(treeItem,headerIndex)
                        dataWidget.loadObject(dataItem)
                        print (treeItem , itemData)
                        self.itemValueUpdated(treeItem,headerIndex,dataItem)


    def saveObject(self): #Forced compatibility with arrays.
        data = []
        for topLevelIndex in range(self.treeWidget.topLevelItemCount()):
            item = self.treeWidget.topLevelItem(topLevelIndex)
            data = data + self.saveTree(item)

        return data

    def saveTree(self,treeItem):
        treeSave = []
        if any(treeItem.widgetsUpdated):
            dataToAdd = {}
            dataToAdd["node"] = localOverride.MiscUtilities.GetObjectName(treeItem.referencedNode)
            for columnIndex in range(1,self.treeWidget.columnCount()):
                itemWidget = self.treeWidget.itemWidget(treeItem,columnIndex)
                dataToAdd[itemWidget.dataName] = itemWidget.saveObject()
            treeSave.append(dataToAdd)

        for i in range(treeItem.childCount()):
            childItem = treeItem.child(i)
            
            childrenData = self.saveTree(childItem)

            if childrenData:
                treeSave = treeSave + childrenData

        return treeSave

    def treeUpdated(self,item,widgetIndex,value):
        item.widgetsUpdated[widgetIndex] = True
        self.itemValueUpdated(item,widgetIndex,value)
        self.OnDataUpdate(self)

    def itemValueUpdated(self,item,widgetIndex,value):
        for i in range(item.childCount()):
            childItem = item.child(i)
            # childItem.userUpdated = False
            childItem.widgetsUpdated[widgetIndex] = False

            widgetToUpdate = self.treeWidget.itemWidget(childItem,widgetIndex)
            widgetToUpdate.loadObject(value)
            self.itemValueUpdated(childItem,widgetIndex,value)

    def createTreeItem(self,treeWidgetParent,node):
        treeItem = EZDataTreeItem(treeWidgetParent,[localOverride.MiscUtilities.GetObjectName(node)],node)

        dataTypes = serverData["ezData"]["dataTypes"]
        # print treeItem
        if self.generic in dataTypes:
            dataType = dataTypes[self.generic]

            columnIndex = 0
            # for fields in dataType:
            for i in range(len(dataType)):
                fields = dataType[i]
                varName = fields["fieldName"]
                varType = fields["fieldType"]
                varValue = fields["fieldValue"]

                if "node" in varName:
                    continue
                else:
                    columnIndex = columnIndex + 1

                self.treeWidget.headerItem().setText(columnIndex, varName)

                dataObject = EZDataObject(dataName=varName,dataType=varType,dataValue=varValue,parent = self )
                # print(fields)
                treeItem.widgetsUpdated.insert(columnIndex,False)
                # print treeItem.widgetsUpdated
                # self.treeUpdated(treeItem,i+1,"LAYOUT")
                dataObject.OnDataUpdate += lambda dataWidget,dataIndex = columnIndex : self.treeUpdated(treeItem,dataIndex,dataWidget.getValue())
                self.treeWidget.setItemWidget(treeItem,columnIndex,dataObject)
        else:
            raise Exception("Tree must be used with dataValues {0} is not valid ".format(self.generic))
        return treeItem

    def buildTree(self,parent,tree):
        for nodeTree in tree:
            if "node" in nodeTree:
                node = nodeTree["node"]
                parentNode = self.createTreeItem(parent,node)
                self.buildTree(parentNode,nodeTree["children"])
            


    def buildLayout(self):
        main_layout = QT.QHBoxLayout()

        self.fieldsContainer = CollapsibleWidget(title=self.dataName,parent = self)
        self.fieldsContainer.setLineWidth(3)
        self.fieldsContainer.setFrameStyle(QT.QFrame.Panel | QT.QFrame.Raised)

        self.treeWidget = QT.QTreeWidget(self.fieldsContainer)
        self.treeWidget.setSizePolicy(QT.QSizePolicy.Expanding, QT.QSizePolicy.MinimumExpanding)
        self.treeWidget.headerItem().setText(0, "node")
        self.treeWidget.setFocusPolicy(QTCore.Qt.StrongFocus)


        parentNode = self.treeWidget
        if "node" in self.treelist:
            node = self.treelist["node"]
            parentNode = self.createTreeItem(self.treeWidget,node)
            parentNode.widgetsUpdated = [True for val in parentNode.widgetsUpdated] # THE ROOT IS ALWAYS SAVED

        # print "AAAAA" , self.treelist
        # print "BBBBB" , self.treelist["node"]
        # print "BBBBB" , self.treelist["children"]

        self.buildTree(parentNode,self.treelist["children"])
        self.fieldsContainer.addWidget(self.treeWidget)
        main_layout.addWidget(self.fieldsContainer)
        self.setLayout(main_layout)
        

class EZDataTreeItem(QT.QTreeWidgetItem):
    referencedNode = None
    isFile = True

    # widgetsUpdated = []

    def __init__(self,tree,columns,node):
        self.referencedNode = node
        super(EZDataTreeItem, self).__init__(tree,columns)
        # super().__init__(tree,columns)
        self.widgetsUpdated = []
        self.widgetsUpdated.append(False)

        self.setFlags(QTCore.Qt.ItemIsEnabled)




#HARDCODED SHIT MUST DIE!
def GetAllChilds1():
    global ParentNode
    # print [localOverride.MiscUtilities.GetObjectName(x) for x in localOverride.MeshesUtilities.GetAllChilds(ParentNode)]
    return [localOverride.MiscUtilities.GetObjectName(x) for x in localOverride.MeshesUtilities.GetAllChilds(ParentNode) 
            if x != ParentNode and 
            localOverride.MeshesUtilities.GetObjectClass(x) not in localOverride.LayersUtilities.exportableParents] if ParentNode else []

def GetAllChilds2():
    global ParentNode
    return [localOverride.MiscUtilities.GetObjectName(x) for x in localOverride.MeshesUtilities.GetAllChilds(ParentNode) 
            if localOverride.MeshesUtilities.GetObjectClass(x) in localOverride.LayersUtilities.exportableParents] if ParentNode else []

def GetAllChilds3():
    global ParentNode
    return [localOverride.MiscUtilities.GetObjectName(x) for x in localOverride.MeshesUtilities.GetAllChilds(ParentNode) 
            if localOverride.MeshesUtilities.GetObjectClass(x) not in localOverride.LayersUtilities.exportableParents
            if "ST_" in localOverride.MiscUtilities.GetObjectName(x)] if ParentNode else [] 

def GetFullTree():
    global ParentNode
    return localOverride.MeshesUtilities.GetSubTree(ParentNode,filt = localOverride.LayersUtilities.exportableParents,includeParent = True) if ParentNode else []