# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\AddProject.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_createNewProjectDialog(object):
    def setupUi(self, createNewProjectDialog):
        createNewProjectDialog.setObjectName("createNewProjectDialog")
        createNewProjectDialog.resize(640, 480)
        createNewProjectDialog.setSizeGripEnabled(True)
        createNewProjectDialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(createNewProjectDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(createNewProjectDialog)
        self.frame.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setLineWidth(1)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget = QtWidgets.QWidget(self.frame)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.projectNameLabel = QtWidgets.QLabel(self.widget)
        self.projectNameLabel.setObjectName("projectNameLabel")
        self.horizontalLayout.addWidget(self.projectNameLabel)
        self.projectNameInput = QtWidgets.QLineEdit(self.widget)
        self.projectNameInput.setObjectName("projectNameInput")
        self.horizontalLayout.addWidget(self.projectNameInput)
        self.verticalLayout_2.addWidget(self.widget)
        spacerItem = QtWidgets.QSpacerItem(20, 189, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.settingsContainer = QtWidgets.QFrame(self.frame)
        self.settingsContainer.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.settingsContainer.setFrameShadow(QtWidgets.QFrame.Raised)
        self.settingsContainer.setObjectName("settingsContainer")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.settingsContainer)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2.addWidget(self.settingsContainer)
        spacerItem1 = QtWidgets.QSpacerItem(20, 188, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.saveButton = QtWidgets.QPushButton(self.frame)
        self.saveButton.setObjectName("saveButton")
        self.verticalLayout_2.addWidget(self.saveButton)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(createNewProjectDialog)
        QtCore.QMetaObject.connectSlotsByName(createNewProjectDialog)

    def retranslateUi(self, createNewProjectDialog):
        _translate = QtCore.QCoreApplication.translate
        createNewProjectDialog.setWindowTitle(_translate("createNewProjectDialog", "Create Project"))
        self.projectNameLabel.setText(_translate("createNewProjectDialog", "Project Name : "))
        self.projectNameInput.setPlaceholderText(_translate("createNewProjectDialog", "Enter a Project name"))
        self.saveButton.setText(_translate("createNewProjectDialog", "Save"))

