from pantheonModules.pantheonUtilities import pantheonHelpers
from pantheonModules.pantheonUtilities import modulesLoader
from pantheonModules.logger.ateneaLogger import AteneaLogger
import sys 

QT = None
QTGui = None
QTCore = None
localOverride = None
mainUIWindow = None

ParentNode = None






def loadUIModules():

    global QT
    global QTGui
    global QTCore
    global localOverride
    global mainUIWindow

    #####HARDCODED SHIT##### HAVE TO DO IT PROPERLY
    global ParentNode

    loader = modulesLoader.ModulesLoader()

    print("EXECUTING OVERRIDE!")
    platform = pantheonHelpers.getPlatformName() 
    if platform == pantheonHelpers.MAX_2018_NAME():
        print("IS MAX 2018!")
        from PySide2 import QtGui,QtCore,QtWidgets
        import MaxPlus

        QT = sys.modules["PySide2.QtWidgets"]
        QTGui = sys.modules["PySide2.QtGui"]
        QTCore = sys.modules["PySide2.QtCore"]
        localOverride = loader("pantheonModules.exporter.overrides.MAXOverrides")

        mainUIWindow = MaxPlus.GetQMaxMainWindow()
        
        selection = localOverride.MiscUtilities.GetCurrentSelection()
        if len(selection) > 0 and localOverride.MeshesUtilities.GetObjectClass(selection[0]) in localOverride.LayersUtilities.exportableParents and not localOverride.MeshesUtilities.GetParent(selection[0]) :
            ParentNode = selection[0]
        else:
            ParentNode = None


    elif platform == pantheonHelpers.MAX_2017_NAME():
        print("IS MAX 2017!")
        from PySide import QtGui,QtCore
        import MaxPlus

        QT = sys.modules["PySide.QtGui"]
        QTGui = sys.modules["PySide.QtGui"]
        QTCore = sys.modules["PySide.QtCore"]
        localOverride = loader("pantheonModules.exporter.overrides.MAXOverrides")

        mainUIWindow = MaxPlus.GetQMaxWindow()

        selection = localOverride.MiscUtilities.GetCurrentSelection()
        if len(selection) > 0 and localOverride.MeshesUtilities.GetObjectClass(selection[0]) in localOverride.LayersUtilities.exportableParents and not localOverride.MeshesUtilities.GetParent(selection[0]) :
            ParentNode = selection[0]
        else:
            ParentNode = None
    
    elif platform == pantheonHelpers.MAYA_NAME():
        print("IS MAYA!")
        from maya import OpenMayaUI as omui 
        from PySide2 import QtGui,QtCore,QtWidgets
        from shiboken2 import wrapInstance

        QT = sys.modules["PySide2.QtWidgets"]
        QTGui = sys.modules["PySide2.QtGui"]
        QTCore = sys.modules["PySide2.QtCore"]
        localOverride = loader("pantheonModules.exporter.overrides.MAYAOverrides")

        from maya import OpenMayaUI as omui
        from shiboken2 import wrapInstance 
        mayaMainWindowPtr = omui.MQtUtil.mainWindow() 
        if mayaMainWindowPtr:
            mayaMainWindow= wrapInstance(long(mayaMainWindowPtr), QT.QMainWindow) 
            mainUIWindow = mayaMainWindow

            selection = localOverride.MiscUtilities.GetCurrentSelection()
            if len(selection) > 0 and localOverride.MeshesUtilities.GetObjectClass(selection[0]) in localOverride.LayersUtilities.exportableParents and not localOverride.MeshesUtilities.GetParent(selection[0]) :
                ParentNode = selection[0]
            else:
                ParentNode = None
        else:
            ParentNode = None
            mainUIWindow = None

    elif platform == pantheonHelpers.BLENDER_279():
        print("IS BLENDER 2.79 ")

        from PySide2 import QtGui,QtCore,QtWidgets
        QT = sys.modules["PySide2.QtWidgets"]
        QTGui = sys.modules["PySide2.QtGui"]
        QTCore = sys.modules["PySide2.QtCore"]
        
        localOverride = loader("pantheonModules.exporter.overrides.BLENDEROverrides")

        app = QT.QApplication.instance()
        if app is None:
            app = QT.QApplication([])
            print("App init")
        else:
            print("App already running.")
        mainUIWindow = None

        selection = localOverride.MiscUtilities.GetCurrentSelection()
        if len(selection) > 0 and localOverride.MeshesUtilities.GetObjectClass(selection[0]) in localOverride.LayersUtilities.exportableParents and not localOverride.MeshesUtilities.GetParent(selection[0]) :
            ParentNode = selection[0]
        else:
            ParentNode = None
    elif platform == pantheonHelpers.BLENDER_280():
        print("IS BLENDER 2.80 ")

        from PySide2 import QtGui,QtCore,QtWidgets
        QT = sys.modules["PySide2.QtWidgets"]
        QTGui = sys.modules["PySide2.QtGui"]
        QTCore = sys.modules["PySide2.QtCore"]
        
        localOverride = loader("pantheonModules.exporter.overrides.BLENDEROverrides")

        app = QT.QApplication.instance()
        if app is None:
            app = QT.QApplication([])
            print("App init")
        else:
            print("App already running.")
        mainUIWindow = None

        selection = localOverride.MiscUtilities.GetCurrentSelection()
        if len(selection) > 0 and localOverride.MeshesUtilities.GetObjectClass(selection[0]) in localOverride.LayersUtilities.exportableParents and not localOverride.MeshesUtilities.GetParent(selection[0]) :
            ParentNode = selection[0]
        else:
            ParentNode = None

    elif platform == pantheonHelpers.NATIVE():
        print("IS NATIVE")

        from PyQt5 import QtCore
        from PyQt5 import QtGui
        from PyQt5 import QtWidgets

        QT = sys.modules["PyQt5.QtWidgets"]
        QTGui = sys.modules["PyQt5.QtGui"]
        QTCore = sys.modules["PyQt5.QtCore"]
        localOverride = None
        mainUIWindow = None

    loader = None

loadUIModules()