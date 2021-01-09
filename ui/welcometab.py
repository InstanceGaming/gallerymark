# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/welcomeTab.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WelcomeTab(object):
    def setupUi(self, WelcomeTab):
        WelcomeTab.setObjectName("WelcomeTab")
        WelcomeTab.resize(394, 624)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(WelcomeTab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.label_2 = QtWidgets.QLabel(WelcomeTab)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 150))
        self.label_2.setLineWidth(1)
        self.label_2.setTextFormat(QtCore.Qt.RichText)
        self.label_2.setScaledContents(True)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.showWelcomeCheckbox = QtWidgets.QCheckBox(WelcomeTab)
        self.showWelcomeCheckbox.setMinimumSize(QtCore.QSize(0, 30))
        self.showWelcomeCheckbox.setChecked(False)
        self.showWelcomeCheckbox.setObjectName("showWelcomeCheckbox")
        self.horizontalLayout.addWidget(self.showWelcomeCheckbox)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(WelcomeTab)
        QtCore.QMetaObject.connectSlotsByName(WelcomeTab)

    def retranslateUi(self, WelcomeTab):
        _translate = QtCore.QCoreApplication.translate
        WelcomeTab.setWindowTitle(_translate("WelcomeTab", "Form"))
        self.label_2.setText(_translate("WelcomeTab", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">To start, open a file (</span><span style=\" font-size:12pt; font-weight:600;\">Ctrl+O</span><span style=\" font-size:12pt;\">) or directory (</span><span style=\" font-size:12pt; font-weight:600;\">Ctrl+D</span><span style=\" font-size:12pt;\">).</span></p><p align=\"center\"><span style=\" font-size:12pt;\">Use the </span><span style=\" font-size:12pt; font-weight:600;\">arrow keys</span><span style=\" font-size:12pt;\"> to navigate pages (</span><span style=\" font-size:12pt; font-weight:600;\">‹›</span><span style=\" font-size:12pt;\">) and change documents (↑↓).</span></p></body></html>"))
        self.showWelcomeCheckbox.setText(_translate("WelcomeTab", "Show welcome tab on startup"))
