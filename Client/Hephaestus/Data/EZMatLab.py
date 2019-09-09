import sys
for module in list(sys.modules):
    if sys.modules[module] and module not in sys.builtin_module_names and "pantheonModules" in str(sys.modules[module]) :
        del(sys.modules[module])

from pantheonModules.ui.data.EZMaterialLibrary import *
from pantheonModules.ui.data.EZMaterialLibrary import EZMaterialLibrary

if __name__ == '__main__' or __name__ == "HephaestusBlender":
    dataEditor = EZMaterialLibrary(parent = mainUIWindow)
    dataEditor.closeInstances(parent = mainUIWindow)
    try:
        dataEditor.buildBaseWindow()
        dataEditor.show()
    except CriticalExportException as cee:
        msg = QT.QMessageBox()
        msg.setIcon(QT.QMessageBox.Critical)
        msg.setWindowTitle(cee.errorFile)
        msg.setText(cee.errormessage)
        msg.setInformativeText("Found critical Error")
        msg.setDetailedText(cee.errorDetails)
        msg.setStandardButtons(QT.QMessageBox.Ok)
        msg.exec_()
    