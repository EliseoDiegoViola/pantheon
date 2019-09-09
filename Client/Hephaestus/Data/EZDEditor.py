import sys
for module in list(sys.modules):
    if sys.modules[module] and module not in sys.builtin_module_names and "pantheonModules" in str(sys.modules[module]) :
        del(sys.modules[module])

from pantheonModules.ui.data.EZDataEditor import *
from pantheonModules.ui.data.EZDataEditor import EzDataEditor



if __name__ == '__main__' or __name__ == "HephaestusBlender":
    try:
        dataEditor = EzDataEditor('ObjectExtraData', parent = mainUIWindow)
        dataEditor.closeInstances(parent = mainUIWindow) 
        print (ParentNode)
        if ParentNode:
            dataEditor.window = dataEditor.setupBaseWindow(0)
        else:
            dataEditor.window = dataEditor.setupErrorWindow()
        dataEditor.show()
    except Exception as e:
        print("Unexpected error:", e)

