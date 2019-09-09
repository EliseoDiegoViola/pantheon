from pantheonModules.exporter.overrides import *
try:
  basestring
except NameError:
  basestring = str


from .DataBase import *

class DataComboBox(DataBase):
    

    def __init__(self,parent = None):
        super(DataComboBox, self).__init__(parent = parent)
        self._widget = ComboBoxNoWeel(parent = parent)
        self._widget.setSizePolicy(QT.QSizePolicy.Expanding, QT.QSizePolicy.Minimum)
        listv = QT.QListView()
        listv.setSpacing(1)
        self._widget.setView(listv)
        self._widget.currentIndexChanged.connect(lambda value : self.OnDataUpdate(self))
        self._widget.setFocusPolicy(QTCore.Qt.StrongFocus)    

    def _getValue(self):
        return self._widget.currentText()

    def _setValue(self,*argv):
        if len(argv) != 1 : raise Exception("DataCheckBox wont accept more than one argument , recieved {0}".format(str(argv)))
        value = argv[0]
        
        if isinstance(value, list):
            for i in range(0,len(value)):
                self._widget.insertItem(i,(value[i]))
        elif isinstance(value, basestring):
            itemIndex = next(iter([i for i in range(self._widget.count()) if self._widget.itemText(i) == value]),None)
            if itemIndex >= 0:
                self._setIndex(itemIndex)

    def _setIndex(self,index):
        self._widget.setCurrentIndex(index)

class ComboBoxNoWeel(QT.QComboBox):

    def __init__(self,parent = None):
        super(ComboBoxNoWeel,self).__init__(parent= parent)

    def wheelEvent(self,event):
        if self.hasFocus():
            self.wheelEvent(event)


