# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'logLocationDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_logLocations(object):
    def setupUi(self, logLocations):
        logLocations.setObjectName("logLocations")
        logLocations.resize(572, 258)
        self.enterLogLocation = QtWidgets.QLineEdit(logLocations)
        self.enterLogLocation.setGeometry(QtCore.QRect(10, 10, 461, 21))
        self.enterLogLocation.setObjectName("enterLogLocation")
        self.logLocationAdd = QtWidgets.QPushButton(logLocations)
        self.logLocationAdd.setGeometry(QtCore.QRect(480, 10, 80, 23))
        self.logLocationAdd.setObjectName("logLocationAdd")
        self.logLocationRemove = QtWidgets.QPushButton(logLocations)
        self.logLocationRemove.setGeometry(QtCore.QRect(480, 40, 80, 23))
        self.logLocationRemove.setObjectName("logLocationRemove")
        self.logLocationExit = QtWidgets.QPushButton(logLocations)
        self.logLocationExit.setGeometry(QtCore.QRect(480, 220, 80, 23))
        self.logLocationExit.setObjectName("logLocationExit")
        self.existingLogLocation = QtWidgets.QListWidget(logLocations)
        self.existingLogLocation.setGeometry(QtCore.QRect(10, 40, 461, 211))
        self.existingLogLocation.setObjectName("existingLogLocation")

        self.retranslateUi(logLocations)
        QtCore.QMetaObject.connectSlotsByName(logLocations)

    def retranslateUi(self, logLocations):
        _translate = QtCore.QCoreApplication.translate
        logLocations.setWindowTitle(_translate("logLocations", "Log Location"))
        self.logLocationAdd.setText(_translate("logLocations", "Add"))
        self.logLocationRemove.setText(_translate("logLocations", "Remove"))
        self.logLocationExit.setText(_translate("logLocations", "Exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    logLocations = QtWidgets.QDialog()
    ui = Ui_logLocations()
    ui.setupUi(logLocations)
    logLocations.show()
    sys.exit(app.exec_())

