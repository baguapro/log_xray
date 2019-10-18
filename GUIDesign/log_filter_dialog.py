# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'logFilterDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_logFilters(object):
    def setupUi(self, logFilters):
        logFilters.setObjectName("logFilters")
        logFilters.resize(693, 389)
        self.filterDisplayName = QtWidgets.QLineEdit(logFilters)
        self.filterDisplayName.setGeometry(QtCore.QRect(130, 10, 441, 23))
        self.filterDisplayName.setObjectName("filterDisplayName")
        self.filterRegexData = QtWidgets.QLineEdit(logFilters)
        self.filterRegexData.setGeometry(QtCore.QRect(130, 50, 441, 23))
        self.filterRegexData.setObjectName("filterRegexData")
        self.filterDisplayNameLabel = QtWidgets.QLabel(logFilters)
        self.filterDisplayNameLabel.setGeometry(QtCore.QRect(30, 10, 91, 20))
        self.filterDisplayNameLabel.setObjectName("filterDisplayNameLabel")
        self.filterRegexLabel = QtWidgets.QLabel(logFilters)
        self.filterRegexLabel.setGeometry(QtCore.QRect(40, 50, 81, 16))
        self.filterRegexLabel.setObjectName("filterRegexLabel")
        self.existingFiltersLabel = QtWidgets.QLabel(logFilters)
        self.existingFiltersLabel.setGeometry(QtCore.QRect(20, 90, 91, 20))
        self.existingFiltersLabel.setObjectName("existingFiltersLabel")
        self.filterAdd = QtWidgets.QPushButton(logFilters)
        self.filterAdd.setGeometry(QtCore.QRect(590, 10, 80, 23))
        self.filterAdd.setObjectName("filterAdd")
        self.filterRemove = QtWidgets.QPushButton(logFilters)
        self.filterRemove.setGeometry(QtCore.QRect(590, 90, 80, 21))
        self.filterRemove.setObjectName("filterRemove")
        self.filterExit = QtWidgets.QPushButton(logFilters)
        self.filterExit.setGeometry(QtCore.QRect(590, 350, 80, 23))
        self.filterExit.setObjectName("filterExit")
        self.existingFilters = QtWidgets.QListWidget(logFilters)
        self.existingFilters.setGeometry(QtCore.QRect(130, 90, 441, 291))
        self.existingFilters.setObjectName("existingFilters")

        self.retranslateUi(logFilters)
        QtCore.QMetaObject.connectSlotsByName(logFilters)

    def retranslateUi(self, logFilters):
        _translate = QtCore.QCoreApplication.translate
        logFilters.setWindowTitle(_translate("logFilters", "Create Log Filters"))
        self.filterDisplayNameLabel.setText(_translate("logFilters", "Display Name"))
        self.filterRegexLabel.setText(_translate("logFilters", "Filter Regex"))
        self.existingFiltersLabel.setText(_translate("logFilters", "Existing Filters"))
        self.filterAdd.setText(_translate("logFilters", "Add"))
        self.filterRemove.setText(_translate("logFilters", "Remove"))
        self.filterExit.setText(_translate("logFilters", "Exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    logFilters = QtWidgets.QDialog()
    ui = Ui_logFilters()
    ui.setupUi(logFilters)
    logFilters.show()
    sys.exit(app.exec_())

