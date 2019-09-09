import sys
import json
import urllib2 as url
import os
import copy
from sets import Set

from pantheonModules.exporter.overrides import *
from pantheonModules.pantheonUtilities import pantheonHelpers
from pantheonModules.logger.ateneaLogger import AteneaLogger


EZToolNotImplementedWindowTitle = "Work In Progress"

class EZToolNotImplemented(object):

    def __init__(self):

        self.parentWindow = None
        self.window = None

    def show(self):
        self.window.show()


    def close(self):
        self.window.close()

    def buildBaseWindow(self):
        window = QT.QScrollArea(self.parentWindow)

        main_layout = QT.QVBoxLayout()
        headerLayout = QT.QHBoxLayout()
        body_layout = QT.QVBoxLayout()

        label = QT.QLabel("THIS TOOL IS NOT YET IMPLEMENTED")
        label.setAlignment(QTCore.Qt.AlignCenter | QTCore.Qt.AlignVCenter)

        headerLayout.addWidget(label)
        main_layout.addLayout(headerLayout)
        main_layout.addLayout(body_layout)

        window.setWindowTitle(EZToolNotImplementedWindowTitle)
        window.setWidgetResizable(False)
        window.setLayout(main_layout)
        return window
    
if __name__ == '__main__':
    notImplemented = EZToolNotImplemented()
    notImplemented.parentWindow = mainUIWindow
    notImplemented.window = notImplemented.buildBaseWindow()
    notImplemented.show()
