from pantheonModules.exporter.overrides import *

### https://github.com/By0ute/pyqt-collapsible-widget

class CollapsibleWidget(QT.QFrame):
    def __init__(self, parent=None, title=None):
        QT.QFrame.__init__(self, parent=parent)
        # QTGui.QFrame.__init__(self,parent)

        self._is_collasped = True
        self._title_frame = None
        self._content, self._content_layout = (None, None)

        self._main_v_layout = QT.QVBoxLayout(self)
        self._main_v_layout.addWidget(self.initTitleFrame(title, self._is_collasped))
        self._main_v_layout.addWidget(self.initContent(self._is_collasped))

        self.initCollapsable()

    def initTitleFrame(self, title, collapsed):
        self._title_frame = self.TitleFrame(title=title, collapsed=collapsed)

        return self._title_frame

    def initContent(self, collapsed):
        self._content = QT.QWidget()
        self._content_layout = QT.QVBoxLayout()

        self._content.setLayout(self._content_layout)
        self._content.setVisible(not collapsed)

        return self._content

    def addWidget(self, widget):
        self._content_layout.addWidget(widget)

    def initCollapsable(self):
        QTCore.QObject.connect(self._title_frame, QTCore.SIGNAL('clicked()'), self.toggleCollapsed)

    def toggleCollapsed(self):
        self._content.setVisible(self._is_collasped)
        self._is_collasped = not self._is_collasped
        self._title_frame._arrow.setArrow(int(self._is_collasped))

    ############################
    #           TITLE          #
    ############################
    class TitleFrame(QT.QFrame):
        def __init__(self, parent=None, title="", collapsed=False):
            QT.QFrame.__init__(self, parent=parent)

            self.setMinimumHeight(24)
            self.move(QTCore.QPoint(24, 0))
            # self.setStyleSheet("border:1px solid rgb(41, 41, 41); ")

            self._hlayout = QT.QHBoxLayout(self)
            self._hlayout.setContentsMargins(0, 0, 0, 0)
            self._hlayout.setSpacing(0)

            self._arrow = None
            self._title = None

            self._hlayout.addWidget(self.initArrow(collapsed))
            self._hlayout.addWidget(self.initTitle(title))

        def initArrow(self, collapsed):
            self._arrow = CollapsibleWidget.Arrow(collapsed=collapsed)
            self._arrow.setStyleSheet("border:0px")

            return self._arrow

        def initTitle(self, title=None):
            self._title = QT.QLabel(title)
            self._title.setMinimumHeight(24)
            self._title.move(QTCore.QPoint(24, 0))
            self._title.setStyleSheet("border:0px")

            return self._title

        def mousePressEvent(self, event):
            self.emit(QTCore.SIGNAL('clicked()'))

            return super(CollapsibleWidget.TitleFrame, self).mousePressEvent(event)


    #############################
    #           ARROW           #
    #############################
    class Arrow(QT.QFrame):
        def __init__(self, parent=None, collapsed=False):
            QT.QFrame.__init__(self, parent=parent)

            self.setMaximumSize(24, 24)

            # horizontal == 0
            self._arrow_horizontal = (QTCore.QPointF(7.0, 8.0), QTCore.QPointF(17.0, 8.0), QTCore.QPointF(12.0, 13.0))
            # vertical == 1
            self._arrow_vertical = (QTCore.QPointF(8.0, 7.0), QTCore.QPointF(13.0, 12.0), QTCore.QPointF(8.0, 17.0))
            # arrow
            self._arrow = None
            self.setArrow(int(collapsed))

        def setArrow(self, arrow_dir):
            if arrow_dir:
                self._arrow = self._arrow_vertical
            else:
                self._arrow = self._arrow_horizontal

        def paintEvent(self, event):
            if QTGui:
                painter = QTGui.QPainter()
                painter.begin(self)
                painter.setBrush(QTGui.QColor(192, 192, 192))
                painter.setPen(QTGui.QColor(64, 64, 64))
                painter.drawPolygon(self._arrow)
                painter.end()
