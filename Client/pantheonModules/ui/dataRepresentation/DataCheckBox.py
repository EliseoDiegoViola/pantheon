from pantheonModules.exporter.overrides import *
from .DataBase import *

class DataCheckBox(DataBase):
    

    def __init__(self,parent = None):
        super(DataCheckBox, self).__init__(parent = parent)
        self._widget = QT.QCheckBox(parent = parent)
        self._widget.setSizePolicy(QT.QSizePolicy.Expanding, QT.QSizePolicy.Minimum)
        self._widget.stateChanged.connect(lambda value : self.OnDataUpdate(self)) 
        self._widget.setFocusPolicy(QTCore.Qt.StrongFocus)

    def _getValue(self):
        check = self._widget.checkState()
        if (check == QTCore.Qt.CheckState.Checked):
            return True; 
        else:
            return False; 

    def _setValue(self,*argv):
        if len(argv) != 1 : raise Exception("DataCheckBox wont accept more than one argument , recieved {0}".format(str(argv)))
        value = argv[0]

        if bool(value):
            self._widget.setCheckState(QTCore.Qt.CheckState.Checked)
        else:
            self._widget.setCheckState(QTCore.Qt.CheckState.Unchecked)
        
            
