import sys
import os
from PyQt5 import QtGui,QtCore,QtWidgets,uic,Qt
from PyQt5.QtWidgets import QApplication,QWidget, QInputDialog, QLineEdit, QFileDialog, QPushButton, QAction, QLineEdit, QMessageBox,QLabel,QHBoxLayout,QVBoxLayout
from enum import Enum
import UI.resources.icons.icons
import UI.resources.fileStatuses.fileStatuses
import UI.resources.statuses.statuses
import json

from .CreateProjectPopup import *
from UI.windows.mainWindow.mainWindow import *
from UI.windows.mainWindow.addProject import *
from pantheonModules.ui.customElements.PathWidget import *
from pantheonModules.pantheonUtilities import events , fileSystemUtilities as fsu , iniConfig


import glob



version = "0.17"
changeLog= """ Window version = {version}:
> Refresh is not implemented
> Filters are not implemented
> Material explorer is not implemented
> Console has no Highlights or links
> DONT EXPORT DIFFERENTS FILE TYPES!

""".format(version=version)

programIconSets = {
    ".max" : ":/icons/max.png",
    ".3ds" : ":/icons/max.png",
    ".ma" : ":/icons/maya.png",
    ".mb" : ":/icons/maya.png",
    ".blend" : ":/icons/blender.png"
}

class FileStatuses(Enum):
    UNKNOWN = ""
    ADDED = ":/fileStatuses/fileAdded.png"
    EXPORTED = ":/fileStatuses/fileExported.png"
    IMPORTED = ":/fileStatuses/fileImported.png"



class MainWindow(QtWidgets.QMainWindow):
    
    filterTags = []
    selectedBuildItems = []
    allFiles = []

    buildStep1Callback = None
    buildStep2Callback = None
    settingsUpdated = None

    consoleMaxLen = 10000


    buildItemsPage = {
    "buildTreeModelPage" : 0,
    "buildFilteredListPage" : 1
    }
#page 1 select
#page 2 search
 

    def __init__(self):
        super().__init__()
        self.mainWindow = Ui_MainWindow()
        self.mainWindow.setupUi(self)
        self.projectSettingsLoaded = events.EventHook()

        self.buttonBuildRefresh = self.mainWindow.buttonBuildRefresh 
        self.buttonBuildStep1 = self.mainWindow.buttonBuildStep1 
        self.buttonBuildStep2 = self.mainWindow.buttonBuildStep2 

        self.projectTitle = self.mainWindow.projectTitle
        self.filtersTree = self.mainWindow.filtersTree
        self.buildNodesTree = self.mainWindow.buildNodesTree
        self.itemsList = self.mainWindow.itemsList
        self.consoleOutput = self.mainWindow.consoleOutput
        self.tabWidget = self.mainWindow.tabWidget
        self.buildProgressBar = self.mainWindow.buildProgressBar
        self.buildFilterSearch = self.mainWindow.buildFilterSearch
        self.buildNodesStackedWidget = self.mainWindow.buildNodesStackedWidget
        self.buildFilteredItemList = self.mainWindow.buildFilteredItemList
        self.buildFilteredItempath = self.mainWindow.buildFilteredItempath
        self.settingsTab=self.mainWindow.settingsTab
        self.buttonApply=self.mainWindow.buttonApply
        self.buttonCancel=self.mainWindow.buttonCancel
        self.projectList = self.mainWindow.projectList
        pathDocuments = os.path.expanduser('~/Documents/')
        self.builderIniPath = pathDocuments + "builder.ini"
        
        
        

      #  self.settingsUpdated= self.mainWindow.settingsUpdated


        self.pathsContainer=self.mainWindow.pathsContainer
        self.fillDataWithBuilderIni()

       



        

        self.buildFilteredItempath.setHidden(True)
        self.warningBox("Atenea Window changelog","Please read carefully",changeLog)

        self.setupStyle()
        self.refreshProjectList()

    #init new fns
    def methodParent(self,object):
        self.globalPaths[object.labelProgram.text()]=object.labelPath.text()
    #finish new fns    

    def setupStyle(self):
        self.buildNodesTree.header().resizeSection(0,375)
        self.buildNodesTree.header().resizeSection(1,75)

    def login(self):
        user = self.mainWindow.userLine.text()
        password = self.mainWindow.passwordLine.text()
        itemsSelected = self.mainWindow.projectList.selectedItems()
        if len(itemsSelected) != 1:
            print("You need to select a project")
            return

        self.warningBox("About to load all project files... ","Ok")
        self.projectSettingsLoaded(itemsSelected[0].settings)
        
        self.mainWindow.atheneaStages.setCurrentIndex(0)


    def connectHandlers(self):
        # self.filtersTree.itemChanged.connect(self.handleFilters)

        #Main Page
        self.buttonApply.clicked.connect(self.applyNewPaths)
        self.buttonCancel.clicked.connect(self.clearPaths)
        self.buildNodesTree.itemChanged.connect(self.handleBuildItems)
        self.buttonBuildRefresh.clicked.connect(lambda : self.warningBox("This feature is not yet implemented","This button should refresh the entire artmaster files in the future"))
        self.buttonBuildStep1.clicked.connect(self.buildStep1)
        self.buttonBuildStep2.clicked.connect(self.buildStep2)
        self.buildFilterSearch.textChanged.connect(lambda : self.updateFilterRegex(self.buildFilterSearch.text()))
        self.buildFilteredItemList.itemClicked.connect(lambda item : self.filteredItemSelected(item))
        self.buildFilteredItemList.itemDoubleClicked.connect(lambda item : self.filteredItemActivated(item))
        self.buildFilteredItemList.itemDoubleClicked.connect(lambda item : self.filteredItemActivated(item))
        self.itemsList.itemDoubleClicked.connect(lambda item : self.addedItemActivated(item))
        
        #Login Page
        self.mainWindow.actionNew_Project.triggered.connect(self.showCreateNewProject)
        self.mainWindow.actionQuit.triggered.connect(lambda : self.warningBox("This feature is not yet implemented","Quit"))
        self.mainWindow.actionAbout_Pantheon.triggered.connect(lambda : self.warningBox("This feature is not yet implemented","About"))
        self.mainWindow.actionReport_an_Issue.triggered.connect(lambda : self.warningBox("This feature is not yet implemented","Report"))
        self.mainWindow.loginButton.clicked.connect(self.login )
        #self.mainWindow.atheneaStages.currentChanged.connect(self.pageChanged)
    
    def showPopUp(self,title,text):
        msg = QT.QMessageBox(self) 
        msg.setIcon(QT.QMessageBox.Information)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStandardButtons(QT.QMessageBox.Ok)
        msg.exec_()

    def applyNewPaths(self):
        import configparser
        config = configparser.ConfigParser()
        config.read(self.builderIniPath)
        config['Paths'] = {}
        objects= {}
        for label, path in  self.globalPaths.items():
            config['Paths'][label]=path
       
        with open(self.builderIniPath, 'w') as configfile:   
            config.write(configfile)
        self.settingsUpdated() 
        self.showPopUp("Apply changes","All changes has been saved and reloaded")  

    def clearPaths(self):
        self.showPopUp("Resets paths","All changes has been discarded and reloaded")  
        for i in range(self.pathsContainer.layout().count()):
            widgetToRemove = self.pathsContainer.layout().itemAt(i).widget()
            if widgetToRemove:
                widgetToRemove.deleteLater()
        self.fillDataWithBuilderIni()
        

    def fillDataWithBuilderIni(self):       
        configFile = iniConfig.AteneaConfig(self.builderIniPath) 
        self.globalPaths = configFile.getMap("Paths")
        for label, path in  self.globalPaths.items():
            add=PathWidget(self.pathsContainer,label,path)
            add.OnDataUpdate+=self.methodParent
            self.pathsContainer.layout().addWidget(add)

    def searchNewPathToBuilder(self,item):
        self.openFileNameDialog()
            #finish settings fn

    def filteredItemSelected(self, item):
        self.buildFilteredItempath.setText(item.referencedFile.relativePath)

    def filteredItemActivated(self,item):
        item.referencedFile.AddToBuildList() 

    def addedItemActivated(self,item):
        item.referencedFile.RemoveFromBuildList() 
        
    def changeSearch(self,page):
        self.buildNodesStackedWidget.setCurrentIndex(page)

    def refreshProjectList(self):
        self.projectList.clear()
        path = os.getenv('APPDATA')+"\\Pantheon\\"
        projectFiles = glob.glob(path+"/*.atnp",recursive=False)
        for pf in projectFiles:
            projectItem = ProjectListItem(pf)
            self.projectList.addItem(projectItem)

        
        print(projectFiles)

    def showCreateNewProject(self):
        createProject = CreateProjectPopUp()
        createProject.exec_()
        self.refreshProjectList()
    # def handleFilters(self, item, column):
    #     tag = item.text(0)
    #     if int(item.checkState(column)) == 2: #Only want fully checked, 1 is only visual (for now) 
    #         if tag not in self.filterTags:
    #             self.filterTags.append(tag)
    #     if int(item.checkState(column)) == 0:
    #         if tag in self.filterTags:
    #             self.filterTags.remove(tag)

    def handleBuildItems(self, item, column):
        tag = item.text(0)
        if type(item) is not ChildTreeItem:
            return

        file = item.referencedFile
        if int(item.checkState(column)) == 2: #Only want fully checked, 1 is only visual (for now)
            file.AddToBuildList() 
        if int(item.checkState(column)) == 0:
            file.RemoveFromBuildList() 



    def updateFilterRegex(self,filt):
        if len(filt) > 1:
            self.buildFilteredItempath.setHidden(False)
            self.buildFilteredItempath.setText("")
            self.changeSearch(self.buildItemsPage["buildFilteredListPage"])
            regex = QtCore.QRegExp(filt)
            searchPattern = filt
            for i in range(self.buildFilteredItemList.count()):
                item = self.buildFilteredItemList.item(i)
                if filt.lower() in item.text().lower():
                    item.setHidden(False)
                else:
                    item.setHidden(True)
        elif len(filt) == 0:
            self.buildFilteredItempath.setHidden(True)
            items = self.buildFilteredItemList.selectedItems()
            for item in items:
                item.referencedFile.ShowItem()
            self.changeSearch(self.buildItemsPage["buildTreeModelPage"])

            searchPattern = filt



    def applyFilter(self):
        pass

    def addToBuildItemsList(self,file):
        self.selectedBuildItems.append(file)

    def removeFromBuildItemsList(self,file):
        self.selectedBuildItems.remove(file)

    def buildStep1(self):
        if self.buildStep1Callback:
            self.buildStep1Callback(self.selectedBuildItems)

    def buildStep2(self):
        if self.buildStep2Callback:
            self.buildStep2Callback(self.selectedBuildItems)


    def warningBox(self,message,information,details = None):
        msgDialog = QtWidgets.QMessageBox()
        msgDialog.setIcon(QtWidgets.QMessageBox.Warning)

        msgDialog.setWindowTitle("Warning")
        msgDialog.setText(message)
        msgDialog.setInformativeText(information)
        
        if details:
            msgDialog.setDetailedText(details)
            msgDialog.setStyleSheet("QLabel{min-width: 150;qproperty-alignment: 'AlignBottom | AlignCenter';}");

        msgDialog.setStandardButtons(QtWidgets.QMessageBox.Ok)
        

        retval = msgDialog.exec_()


    def logConsoleOutput(self,message):
        currentText = self.consoleOutput.text()

        if len(currentText) > self.consoleMaxLen:
            currentText = currentText[(len(message) + 4):]
        currentText = currentText+"<br>"+ message
        self.consoleOutput.setText(currentText)

    def showProgress(self,value,message):
        if message:
            self.buildProgressBar.setHidden(False)
            value = value *100
            self.buildProgressBar.setValue(value)
            self.buildProgressBar.setFormat("%p% {0}".format(message))
        else:
            self.buildProgressBar.setHidden(True)

    #FILTER IS OUT FOR BAD NOMENCLATURE 
    def loadFiles(self,files):
        rootBuildTree = {}
        rootBuildTree["TREEITEM"] = self.buildNodesTree

        rootFilterTree = {}
        rootFilterTree["TREEITEM"] = self.filtersTree

        itemList = self.itemsList
        filteredList = self.buildFilteredItemList

        self.allFiles = []

        for file in files:
            buildLookingIn = rootBuildTree
            # filterLookingIn = rootFilterTree
            newFile = file 
            self.allFiles.append(newFile)
            for tag in newFile.tags:
                if tag in buildLookingIn.keys():
                    buildLookingIn = buildLookingIn[tag]
                    # filterLookingIn = filterLookingIn[tag]
                else:
                    buildLookingIn[tag] = {}
                    folderUIItem = ParentTreeItem(buildLookingIn["TREEITEM"], [tag])
                    buildLookingIn[tag]["TREEITEM"] = folderUIItem
                    buildLookingIn = buildLookingIn[tag]



                    # filterLookingIn[tag] = {}
                    # filterUIItem = None
                    # if tag == newFile.tags[-1]:
                    #     filterUIItem = FilterTreeFolder(filterLookingIn["TREEITEM"], [tag])
                    # else:
                    #     filterUIItem = FilterTreeItem(filterLookingIn["TREEITEM"], [tag])

                    # filterLookingIn[tag]["TREEITEM"] = filterUIItem
                    # filterLookingIn = filterLookingIn[tag]

            buildTreeitem = ChildTreeItem(buildLookingIn["TREEITEM"], [newFile.fileName],newFile)

            buildListItem = ItemToBuild(newFile)
            itemList.addItem(buildListItem)
            buildListItem.setHidden(True)

            filteresListItem = FilteredItem(newFile)
            filteredList.addItem(filteresListItem)

            newFile.OnBuildQueueRemoved += self.removeFromBuildItemsList
            newFile.OnBuildQueueRemoved += lambda f, item=buildListItem: item.setHidden(True)
            newFile.OnBuildQueueRemoved += lambda f, item=buildTreeitem: item.setCheckState(0,0)
            # newFile.OnBuildQueueRemoved += lambda f, item=filteresListItem: item.setCheckState(0,0)
        
            newFile.OnBuildQueueAdded += self.addToBuildItemsList
            newFile.OnBuildQueueAdded += lambda f, item=buildListItem: item.setHidden(False)
            newFile.OnBuildQueueAdded += lambda f, item=buildTreeitem: item.setCheckState(0,2)
            # newFile.OnBuildQueueAdded += lambda f, item=filteresListItem: item.setCheckState(0,0)

            newFile.OnShowItem += lambda f, item=buildTreeitem: item.expandTree(True)

            newFile.OnStatusUpdated += lambda f, item=buildTreeitem: item.changeStatus(True)



class ParentTreeItem(QtWidgets.QTreeWidgetItem):
    isFile = False

    def __init__(self,tree,columns):
        super().__init__(tree,columns)
        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/folderIcon.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.setIcon(0,icon)
        

    def expandTree(self,expand):
        self.setExpanded(expand)
        parent = self.parent()
        if parent:
            parent.expandTree(expand)

class ChildTreeItem(QtWidgets.QTreeWidgetItem):
    referencedFile = None
    isFile = True

    def __init__(self,tree,columns,file):
        self.referencedFile = file
        super().__init__(tree,columns)
        self.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)
        self.setCheckState(0, QtCore.Qt.Unchecked)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(programIconSets[file.fileExtension]), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.setIcon(0,icon)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(file.currentStatus.value), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.setIcon(1,icon)

    def expandTree(self,expand):
        self.setExpanded(expand)
        parent = self.parent()
        if parent:
            parent.expandTree(expand)
        
    def changeStatus(self,status):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(status.value), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.setIcon(1,icon)


class ItemToBuild(QtWidgets.QListWidgetItem):
    referencedFile = None
    readyToBuild = True

    def __init__(self,file):
        self.referencedFile = file
        super().__init__(file.fileName)
        self.setFlags( QtCore.Qt.ItemIsEnabled)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(programIconSets[file.fileExtension]), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.setIcon(icon)

class FilteredItem(QtWidgets.QListWidgetItem):
    referencedFile = None
    isFile = True

    def __init__(self,file):
        self.referencedFile = file
        super().__init__(file.fileName)
        self.setFlags( QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(programIconSets[file.fileExtension]), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.setIcon(icon)
        
    

class FilterTreeItem(QtWidgets.QTreeWidgetItem):
    def __init__(self,tree,columns):
        super().__init__(tree,columns)
        self.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)
        self.setCheckState(0, QtCore.Qt.Unchecked)

class FilterTreeFolder(QtWidgets.QTreeWidgetItem):
    def __init__(self,tree,columns):
        super().__init__(tree,columns)
        self.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)
        self.setCheckState(0, QtCore.Qt.Unchecked)

class ProjectListItem(QtWidgets.QListWidgetItem):
    settings = None
    

    def __init__(self,projectFile):
        self.referencedFile = projectFile
        super().__init__(self.referencedFile)
        #self.setFlags( QtCore.Qt.ItemIsEnabled)

        with open(self.referencedFile) as data_file:    
            self.settings = json.load(data_file)

        #icon = QtGui.QIcon()
        #icon.addPixmap(QtGui.QPixmap(programIconSets[file.fileExtension]), QtGui.QIcon.Normal, QtGui.QIcon.On)
        #self.setIcon(icon)



def ShowUI(step1Callback, step2Callback,logConsoleEvent,progressReportEvent,settingsUpdated):
    # thisFilePath = os.path.realpath(__file__)
    # windowsPath = os.path.dirname(os.path.dirname(thisFilePath)) + "\\Windows"
    mainWindow = MainWindow()
    mainWindow.buildStep1Callback = step1Callback
    mainWindow.buildStep2Callback = step2Callback
    mainWindow.settingsUpdated = settingsUpdated

    logConsoleEvent += mainWindow.logConsoleOutput
    progressReportEvent += mainWindow.showProgress
    #
    mainWindow.connectHandlers()

    #settingsTab = ContentSettings(mainWindow.settingsTab,mainWindow.settingsUpdated)
    return mainWindow
    # allFiles = fetchFiles(artmastersPath,('/**/*.ma','/**/*.mb','/**/*.blend','/**/*.max','/**/*.3ds'))
    
    # print("READY")
    
    
    
# if __name__ == '__main__':
#     ShowUI(closedWindowCallback = (lambda : sys.exit(0)))

    



