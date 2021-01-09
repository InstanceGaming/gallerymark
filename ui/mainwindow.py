# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        MainWindow.setMinimumSize(QtCore.QSize(640, 480))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QtCore.QSize(100, 100))
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.leftPane = QtWidgets.QWidget(self.splitter)
        self.leftPane.setMinimumSize(QtCore.QSize(200, 0))
        self.leftPane.setMaximumSize(QtCore.QSize(400, 16777215))
        self.leftPane.setObjectName("leftPane")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.leftPane)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.leftPane)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(False)
        self.tabWidget.setObjectName("tabWidget")
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.splitter)
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.rightPane = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.rightPane.setContentsMargins(0, 0, 0, 0)
        self.rightPane.setSpacing(0)
        self.rightPane.setObjectName("rightPane")
        self.toolbar = QtWidgets.QWidget(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolbar.sizePolicy().hasHeightForWidth())
        self.toolbar.setSizePolicy(sizePolicy)
        self.toolbar.setMinimumSize(QtCore.QSize(100, 25))
        self.toolbar.setMaximumSize(QtCore.QSize(16777215, 30))
        self.toolbar.setObjectName("toolbar")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.toolbar)
        self.horizontalLayout.setContentsMargins(9, 0, 9, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.resetViewBtn = QtWidgets.QToolButton(self.toolbar)
        self.resetViewBtn.setObjectName("resetViewBtn")
        self.horizontalLayout_2.addWidget(self.resetViewBtn)
        self.zoomInBtn = QtWidgets.QToolButton(self.toolbar)
        self.zoomInBtn.setObjectName("zoomInBtn")
        self.horizontalLayout_2.addWidget(self.zoomInBtn)
        self.zoomOutBtn = QtWidgets.QToolButton(self.toolbar)
        self.zoomOutBtn.setObjectName("zoomOutBtn")
        self.horizontalLayout_2.addWidget(self.zoomOutBtn)
        self.penBtn = QtWidgets.QToolButton(self.toolbar)
        self.penBtn.setCheckable(True)
        self.penBtn.setObjectName("penBtn")
        self.horizontalLayout_2.addWidget(self.penBtn)
        self.eraserBtn = QtWidgets.QToolButton(self.toolbar)
        self.eraserBtn.setCheckable(True)
        self.eraserBtn.setAutoExclusive(False)
        self.eraserBtn.setObjectName("eraserBtn")
        self.horizontalLayout_2.addWidget(self.eraserBtn)
        self.toolSizeText = QtWidgets.QLabel(self.toolbar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolSizeText.sizePolicy().hasHeightForWidth())
        self.toolSizeText.setSizePolicy(sizePolicy)
        self.toolSizeText.setText("")
        self.toolSizeText.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.toolSizeText.setObjectName("toolSizeText")
        self.horizontalLayout_2.addWidget(self.toolSizeText)
        self.pageCountText = QtWidgets.QLabel(self.toolbar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pageCountText.sizePolicy().hasHeightForWidth())
        self.pageCountText.setSizePolicy(sizePolicy)
        self.pageCountText.setMinimumSize(QtCore.QSize(50, 0))
        self.pageCountText.setMaximumSize(QtCore.QSize(150, 16777215))
        self.pageCountText.setTextFormat(QtCore.Qt.PlainText)
        self.pageCountText.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.pageCountText.setObjectName("pageCountText")
        self.horizontalLayout_2.addWidget(self.pageCountText)
        self.horizontalLayout.addLayout(self.horizontalLayout_2)
        self.rightPane.addWidget(self.toolbar)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.prevPageBtn = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.prevPageBtn.sizePolicy().hasHeightForWidth())
        self.prevPageBtn.setSizePolicy(sizePolicy)
        self.prevPageBtn.setMaximumSize(QtCore.QSize(10, 150))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.prevPageBtn.setFont(font)
        self.prevPageBtn.setFlat(True)
        self.prevPageBtn.setObjectName("prevPageBtn")
        self.horizontalLayout_3.addWidget(self.prevPageBtn)
        self.pageViewer = PageViewer(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.pageViewer.sizePolicy().hasHeightForWidth())
        self.pageViewer.setSizePolicy(sizePolicy)
        self.pageViewer.setMinimumSize(QtCore.QSize(100, 100))
        self.pageViewer.setObjectName("pageViewer")
        self.horizontalLayout_3.addWidget(self.pageViewer)
        self.nextPageBtn = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.nextPageBtn.sizePolicy().hasHeightForWidth())
        self.nextPageBtn.setSizePolicy(sizePolicy)
        self.nextPageBtn.setMaximumSize(QtCore.QSize(10, 150))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.nextPageBtn.setFont(font)
        self.nextPageBtn.setDefault(False)
        self.nextPageBtn.setFlat(True)
        self.nextPageBtn.setObjectName("nextPageBtn")
        self.horizontalLayout_3.addWidget(self.nextPageBtn)
        self.rightPane.addLayout(self.horizontalLayout_3)
        self.verticalLayout.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 20))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        self.menuGallerymark = QtWidgets.QMenu(self.menubar)
        self.menuGallerymark.setObjectName("menuGallerymark")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionFileOpen = QtWidgets.QAction(MainWindow)
        self.actionFileOpen.setAutoRepeat(False)
        self.actionFileOpen.setObjectName("actionFileOpen")
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.actionFileClose = QtWidgets.QAction(MainWindow)
        self.actionFileClose.setEnabled(False)
        self.actionFileClose.setAutoRepeat(False)
        self.actionFileClose.setObjectName("actionFileClose")
        self.actionZoomIn = QtWidgets.QAction(MainWindow)
        self.actionZoomIn.setEnabled(False)
        self.actionZoomIn.setAutoRepeat(False)
        self.actionZoomIn.setObjectName("actionZoomIn")
        self.actionZoomOut = QtWidgets.QAction(MainWindow)
        self.actionZoomOut.setEnabled(False)
        self.actionZoomOut.setAutoRepeat(False)
        self.actionZoomOut.setObjectName("actionZoomOut")
        self.actionPenTool = QtWidgets.QAction(MainWindow)
        self.actionPenTool.setCheckable(True)
        self.actionPenTool.setEnabled(False)
        self.actionPenTool.setAutoRepeat(False)
        self.actionPenTool.setObjectName("actionPenTool")
        self.actionDirectoryOpen = QtWidgets.QAction(MainWindow)
        self.actionDirectoryOpen.setAutoRepeat(False)
        self.actionDirectoryOpen.setObjectName("actionDirectoryOpen")
        self.actionDirectoryClose = QtWidgets.QAction(MainWindow)
        self.actionDirectoryClose.setEnabled(False)
        self.actionDirectoryClose.setAutoRepeat(False)
        self.actionDirectoryClose.setObjectName("actionDirectoryClose")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setShortcut("")
        self.actionExit.setAutoRepeat(False)
        self.actionExit.setMenuRole(QtWidgets.QAction.QuitRole)
        self.actionExit.setObjectName("actionExit")
        self.actionFileSave = QtWidgets.QAction(MainWindow)
        self.actionFileSave.setObjectName("actionFileSave")
        self.actionNextPage = QtWidgets.QAction(MainWindow)
        self.actionNextPage.setObjectName("actionNextPage")
        self.actionPreviousPage = QtWidgets.QAction(MainWindow)
        self.actionPreviousPage.setObjectName("actionPreviousPage")
        self.actionDarkTheme = QtWidgets.QAction(MainWindow)
        self.actionDarkTheme.setCheckable(True)
        self.actionDarkTheme.setObjectName("actionDarkTheme")
        self.actionUndo = QtWidgets.QAction(MainWindow)
        self.actionUndo.setEnabled(False)
        self.actionUndo.setObjectName("actionUndo")
        self.actionRedo = QtWidgets.QAction(MainWindow)
        self.actionRedo.setEnabled(False)
        self.actionRedo.setObjectName("actionRedo")
        self.actionResetView = QtWidgets.QAction(MainWindow)
        self.actionResetView.setObjectName("actionResetView")
        self.actionEraserTool = QtWidgets.QAction(MainWindow)
        self.actionEraserTool.setCheckable(True)
        self.actionEraserTool.setEnabled(False)
        self.actionEraserTool.setAutoRepeat(False)
        self.actionEraserTool.setObjectName("actionEraserTool")
        self.actionDirectoryRefresh = QtWidgets.QAction(MainWindow)
        self.actionDirectoryRefresh.setEnabled(False)
        self.actionDirectoryRefresh.setObjectName("actionDirectoryRefresh")
        self.actionNextFile = QtWidgets.QAction(MainWindow)
        self.actionNextFile.setEnabled(False)
        self.actionNextFile.setObjectName("actionNextFile")
        self.actionPreviousFile = QtWidgets.QAction(MainWindow)
        self.actionPreviousFile.setEnabled(False)
        self.actionPreviousFile.setObjectName("actionPreviousFile")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionWelcomeTab = QtWidgets.QAction(MainWindow)
        self.actionWelcomeTab.setObjectName("actionWelcomeTab")
        self.actionCloseOpenFiles = QtWidgets.QAction(MainWindow)
        self.actionCloseOpenFiles.setEnabled(False)
        self.actionCloseOpenFiles.setObjectName("actionCloseOpenFiles")
        self.actionSaveOpenFiles = QtWidgets.QAction(MainWindow)
        self.actionSaveOpenFiles.setEnabled(False)
        self.actionSaveOpenFiles.setObjectName("actionSaveOpenFiles")
        self.actionShowExplorer = QtWidgets.QAction(MainWindow)
        self.actionShowExplorer.setEnabled(False)
        self.actionShowExplorer.setObjectName("actionShowExplorer")
        self.menuFile.addAction(self.actionFileOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionFileSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionFileClose)
        self.menuView.addAction(self.actionZoomIn)
        self.menuView.addAction(self.actionZoomOut)
        self.menuView.addAction(self.actionResetView)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionNextPage)
        self.menuView.addAction(self.actionPreviousPage)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionWelcomeTab)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionDarkTheme)
        self.menuTools.addAction(self.actionPenTool)
        self.menuTools.addAction(self.actionEraserTool)
        self.menuGallerymark.addAction(self.actionDirectoryOpen)
        self.menuGallerymark.addSeparator()
        self.menuGallerymark.addAction(self.actionPreviousFile)
        self.menuGallerymark.addAction(self.actionNextFile)
        self.menuGallerymark.addAction(self.actionSaveOpenFiles)
        self.menuGallerymark.addAction(self.actionCloseOpenFiles)
        self.menuGallerymark.addSeparator()
        self.menuGallerymark.addAction(self.actionDirectoryRefresh)
        self.menuGallerymark.addAction(self.actionShowExplorer)
        self.menuGallerymark.addAction(self.actionDirectoryClose)
        self.menuGallerymark.addSeparator()
        self.menuGallerymark.addAction(self.actionExit)
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuGallerymark.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.resetViewBtn.setText(_translate("MainWindow", "Reset View"))
        self.zoomInBtn.setText(_translate("MainWindow", "Zoom In"))
        self.zoomOutBtn.setText(_translate("MainWindow", "Zoom Out"))
        self.penBtn.setText(_translate("MainWindow", "&Pen Tool"))
        self.eraserBtn.setText(_translate("MainWindow", "&Eraser Tool"))
        self.pageCountText.setText(_translate("MainWindow", "Page 1 of ?"))
        self.prevPageBtn.setText(_translate("MainWindow", "<"))
        self.nextPageBtn.setText(_translate("MainWindow", ">"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.menuTools.setTitle(_translate("MainWindow", "&Tools"))
        self.menuGallerymark.setTitle(_translate("MainWindow", "GalleryMark"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionFileOpen.setText(_translate("MainWindow", "Open..."))
        self.actionFileOpen.setToolTip(_translate("MainWindow", "Open a file"))
        self.actionFileOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.action.setText(_translate("MainWindow", "-"))
        self.actionFileClose.setText(_translate("MainWindow", "Close"))
        self.actionFileClose.setToolTip(_translate("MainWindow", "Close opened file"))
        self.actionFileClose.setShortcut(_translate("MainWindow", "Ctrl+Shift+O"))
        self.actionZoomIn.setText(_translate("MainWindow", "Zoom In"))
        self.actionZoomIn.setToolTip(_translate("MainWindow", "Zoom further into document"))
        self.actionZoomIn.setShortcut(_translate("MainWindow", "Ctrl+="))
        self.actionZoomOut.setText(_translate("MainWindow", "Zoom Out"))
        self.actionZoomOut.setToolTip(_translate("MainWindow", "Zoom out of document"))
        self.actionZoomOut.setShortcut(_translate("MainWindow", "Ctrl+-"))
        self.actionPenTool.setText(_translate("MainWindow", "Pen"))
        self.actionPenTool.setToolTip(_translate("MainWindow", "Toggle the pen tool"))
        self.actionPenTool.setShortcut(_translate("MainWindow", "P"))
        self.actionDirectoryOpen.setText(_translate("MainWindow", "Open directory..."))
        self.actionDirectoryOpen.setToolTip(_translate("MainWindow", "Open a directory"))
        self.actionDirectoryOpen.setShortcut(_translate("MainWindow", "Ctrl+D"))
        self.actionDirectoryClose.setText(_translate("MainWindow", "Close directory"))
        self.actionDirectoryClose.setToolTip(_translate("MainWindow", "Close open directory"))
        self.actionDirectoryClose.setShortcut(_translate("MainWindow", "Ctrl+Shift+D"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setToolTip(_translate("MainWindow", "Exit this program"))
        self.actionFileSave.setText(_translate("MainWindow", "Save"))
        self.actionFileSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionNextPage.setText(_translate("MainWindow", "Next page"))
        self.actionNextPage.setShortcut(_translate("MainWindow", "Right"))
        self.actionPreviousPage.setText(_translate("MainWindow", "Previous page"))
        self.actionPreviousPage.setShortcut(_translate("MainWindow", "Left"))
        self.actionDarkTheme.setText(_translate("MainWindow", "Dark theme"))
        self.actionUndo.setText(_translate("MainWindow", "Undo"))
        self.actionUndo.setShortcut(_translate("MainWindow", "Ctrl+Z"))
        self.actionRedo.setText(_translate("MainWindow", "Redo"))
        self.actionRedo.setShortcut(_translate("MainWindow", "Ctrl+Shift+Z"))
        self.actionResetView.setText(_translate("MainWindow", "Reset view"))
        self.actionEraserTool.setText(_translate("MainWindow", "Eraser"))
        self.actionEraserTool.setToolTip(_translate("MainWindow", "Toggle the eraser tool"))
        self.actionEraserTool.setShortcut(_translate("MainWindow", "E"))
        self.actionDirectoryRefresh.setText(_translate("MainWindow", "Refresh"))
        self.actionDirectoryRefresh.setShortcut(_translate("MainWindow", "F5"))
        self.actionNextFile.setText(_translate("MainWindow", "Next"))
        self.actionNextFile.setShortcut(_translate("MainWindow", "Down"))
        self.actionPreviousFile.setText(_translate("MainWindow", "Previous"))
        self.actionPreviousFile.setShortcut(_translate("MainWindow", "Up"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAbout.setShortcut(_translate("MainWindow", "F1"))
        self.actionWelcomeTab.setText(_translate("MainWindow", "Welcome tab"))
        self.actionCloseOpenFiles.setText(_translate("MainWindow", "Close open files"))
        self.actionCloseOpenFiles.setShortcut(_translate("MainWindow", "Ctrl+Alt+D"))
        self.actionSaveOpenFiles.setText(_translate("MainWindow", "Save open files"))
        self.actionSaveOpenFiles.setShortcut(_translate("MainWindow", "Ctrl+Alt+S"))
        self.actionShowExplorer.setText(_translate("MainWindow", "Show in explorer"))
        self.actionShowExplorer.setShortcut(_translate("MainWindow", "Ctrl+E"))
from pageviewer import PageViewer
