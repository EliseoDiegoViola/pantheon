from pantheonModules.exporter.overrides import *
from .DataBase import *

class DataTextField(DataBase):
    

    def __init__(self,parent = None):
        super(DataTextField, self).__init__(parent = parent)
        self._widget = QT.QLineEdit(parent = parent)
        self._widget.setSizePolicy(QT.QSizePolicy.Expanding, QT.QSizePolicy.Minimum)
        self._widget.editingFinished.connect(lambda : self.OnDataUpdate(self))
        self._widget.setFocusPolicy(QTCore.Qt.StrongFocus)
        # self._widget.installEventFilter(self)
        
    def _getValue(self):
        return self._widget.text()

    def _setValue(self,*argv):
        if len(argv) != 1 : raise Exception("DataCheckBox wont accept more than one argument , recieved {0}".format(str(argv)))
        value = argv[0]

        self._widget.setText(str(value))


    