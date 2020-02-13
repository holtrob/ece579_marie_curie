# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'marie_curie_gui.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(30, 20, 331, 111))
        self.groupBox.setObjectName("groupBox")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(180, 80, 141, 23))
        self.pushButton.setObjectName("pushButton")
        self.formLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.formLayoutWidget.setGeometry(QtCore.QRect(40, 30, 231, 31))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.expressionLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.expressionLabel.setObjectName("expressionLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.expressionLabel)
        self.expressionComboBox = QtWidgets.QComboBox(self.formLayoutWidget)
        self.expressionComboBox.setObjectName("expressionComboBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.expressionComboBox)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menubar.setObjectName("menubar")
        self.menuExpressions_and_Gestures_Panel = QtWidgets.QMenu(self.menubar)
        self.menuExpressions_and_Gestures_Panel.setObjectName("menuExpressions_and_Gestures_Panel")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuExpressions_and_Gestures_Panel.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Expressions and Gestures"))
        self.pushButton.setText(_translate("MainWindow", "Perform Expression"))
        self.expressionLabel.setText(_translate("MainWindow", "Expression"))
        self.menuExpressions_and_Gestures_Panel.setTitle(_translate("MainWindow", "Expressions and Gestures Panel"))
