import logging
import os
import sys
import argparse
import fitz
import webbrowser
from enum import IntEnum
from pathlib import Path

import qdarkstyle

from PyQt5.QtCore import QPoint, Qt, QEvent, QCoreApplication, QSettings
from PyQt5.QtGui import QPixmap, QColor, QPainter, QStandardItem, QStandardItemModel, QKeySequence, QIcon
from PyQt5.QtWidgets import (QApplication, QLabel, QDesktopWidget, QMainWindow, QFileDialog, QWidget,
                             QVBoxLayout, QListView, QTabWidget, QMessageBox, QDialog, QUndoStack,
                             QUndoCommand, QErrorMessage)

from utils import (get_download_path, generateDrawingPixmap, qtPixmapToJPG, get_file_size, format_file_size,
                   resource_path)

from ui.mainwindow import Ui_MainWindow
from ui.welcometab import Ui_WelcomeTab
from ui.about import Ui_About

APP_VERSION = '1.0.1'
APP_ICON = 'gallerymark.ico'
APP_ORG = 'GalleryMark'
APP_WEBSITE = 'https://github.com/InstanceGaming/gallerymark'
APP_NAME = 'GalleryMark'


class ToolMode(IntEnum):
    NOTHING = 0
    DRAGGING = 1
    PEN = 2
    ERASER = 3


class DrawCommand(QUndoCommand):

    @property
    def viewer(self):
        return self._viewer

    @property
    def before(self):
        return self._pixmap_before

    @property
    def current(self):
        return self._current

    def __init__(self, page_viewer, pixmap_before):
        super().__init__()
        self.setText('Draw')

        self._viewer = page_viewer
        self._before = pixmap_before
        self._current = self._viewer.page.drawing_image

    def undo(self):
        self._viewer.page.setDrawingPixmap(self._before)
        self._viewer.updateDrawingLayer()

    def redo(self):
        self._viewer.page.setDrawingPixmap(self._current)
        self._viewer.updateDrawingLayer()


class GMPage:

    @property
    def document(self):
        return self._doc

    @property
    def index(self):
        return self._index

    @property
    def page_image(self):
        return self._page_image

    @property
    def drawing_image(self):
        return self._drawing_image

    @property
    def command_count(self):
        return self._undo_stack.count()

    @property
    def can_undo(self):
        return self._undo_stack.canUndo()

    @property
    def can_redo(self):
        return self._undo_stack.canRedo()

    def __init__(self, document, mu_page, index):
        assert isinstance(document, GMDoc)
        assert isinstance(mu_page, fitz.Page)
        assert type(index) is int

        self._doc = document
        self._index = index

        self._mu_page = mu_page

        # zoom in to get higher resolution pixmap
        zoom = 2
        matrix = fitz.Matrix(zoom, zoom)

        page_data = self._mu_page.getPixmap(matrix=matrix, alpha=False).getImageData()

        self._undo_stack = QUndoStack()

        self._page_image = QPixmap()
        self._page_image.loadFromData(page_data)
        self._drawing_image = generateDrawingPixmap(self._page_image)
        self._last_drawing_hash = None

        self.captureState()

    def getData(self, alpha=False):
        return self._mu_page.getPixmap(alpha=alpha).getImageData()

    def getSize(self):
        return self._page_image.size()

    def setDrawingPixmap(self, pixmap):
        self._drawing_image = pixmap

    def getMergedPixmap(self):
        result = QPixmap(self.getSize())
        result.fill(QColor(255, 255, 255))

        painter = QPainter(result)
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
        painter.drawPixmap(QPoint(0, 0), self._page_image)
        painter.drawPixmap(QPoint(0, 0), self._drawing_image)
        painter.end()

        return result

    def getUndoAction(self, parent):
        return self._undo_stack.createUndoAction(parent)

    def getRedoAction(self, parent):
        return self._undo_stack.createRedoAction(parent)

    def pushCommand(self, command):
        assert isinstance(command, QUndoCommand)
        self._undo_stack.push(command)

    def captureState(self):
        self._last_drawing_hash = self._drawing_image.cacheKey()
        self._undo_stack.setClean()

    def changed(self):
        if self._undo_stack.isClean():
            return False

        return self._undo_stack.count() > 0

    def undo(self):
        self._undo_stack.undo()

    def redo(self):
        self._undo_stack.redo()


class GMDoc:

    @property
    def path(self):
        return self._path

    @property
    def directory(self):
        return os.path.dirname(self._path)

    @property
    def name(self):
        return Path(self._path).name

    @property
    def is_open(self):
        return self._mu_doc is not None and not self._mu_doc.isClosed

    def __init__(self, path):
        self._path = path
        self._mu_doc = None

        self._pages = []

    def open(self):
        self._mu_doc = fitz.open(self._path)

    def getPageCount(self):
        return self._mu_doc.pageCount if self.is_open else None

    def getPage(self, i):
        if self.is_open:
            for p in self._pages:
                if p.index == i:
                    return p

            mu_page = self._mu_doc.loadPage(i)

            if mu_page is not None:
                page = GMPage(self, mu_page, i)
                self._pages.append(page)
                return page
        return None

    def loadRemainingPages(self):
        existing_indices = [ep.index for ep in self._pages]
        loaded_pages = []
        indices = list(range(self.getPageCount()))

        for i in indices:
            if i in existing_indices:
                continue
            loaded_pages.append(self.getPage(i))

        return loaded_pages

    def getSaveFilename(self):
        split = os.path.splitext(self.name)
        name = split[0]
        ext = split[1]
        return '{} (Graded){}'.format(name, ext)

    def getSavePath(self):
        return os.path.join(self.directory, self.getSaveFilename())

    def saveDrawingPDF(self):
        if len(self._pages) > 0:
            self.loadRemainingPages()

            doc = fitz.Document()

            for page in self._pages:
                s = page.getSize()
                w = s.width()
                h = s.height()
                i = page.index
                p = doc.newPage(i, w, h)

                pixmap = page.getMergedPixmap()
                image_data = qtPixmapToJPG(pixmap)

                p.insertImage(fitz.Rect((0, 0), (w, h)), stream=image_data)

            doc.save(self.getSavePath())

        for page in self._pages:
            page.captureState()

    def changed(self):
        for page in self._pages:
            if page.changed():
                return True
        return False

    def close(self, force=False):
        if self.changed() and not force:
            mb = QMessageBox()
            mb.setText('Unsaved Changes')
            mb.setInformativeText('Do you want to save changes to "{}"?'.format(self.name))
            mb.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            mb.setDefaultButton(QMessageBox.Save)
            result = mb.exec()

            if result == QMessageBox.Cancel:
                return False
            elif result == QMessageBox.Save:
                self.saveDrawingPDF()

        if self.is_open:
            self._mu_doc.close()

        return True


class GMDir:
    EXT_WHITELIST = '.pdf'

    @property
    def path(self):
        return self._path

    @property
    def documents(self):
        return self._documents

    @property
    def name(self):
        return self._name

    @property
    def tab_index(self):
        return self._tab_index

    @property
    def closed(self):
        return self._closed

    @property
    def open_count(self):
        return self._open_count

    @property
    def unsaved_count(self):
        return self._unsaved_count

    def __init__(self, gm, path):
        assert isinstance(gm, GalleryMark)
        self._gm = gm
        self._path = path
        self._name = os.path.basename(path)
        self._documents = []
        self._open_count = 0
        self._unsaved_count = 0

        self._tab_index = None
        self._tab_widget = None

        self._listview = QListView()
        self._listview.setViewMode(QListView.ListMode)
        self._listview.setSelectionBehavior(QListView.SelectRows)
        self._listview.activated.connect(self.onListViewItemActivated)

        self._active_document = None

        self._closed = False
        self.refresh(init=True)

    def refresh(self, init=False):
        to_remove = []
        for doc in self._documents:
            if not os.path.exists(doc.path):
                to_remove.append(doc)

        for r in to_remove:
            self._documents.remove(r)

        for item in os.listdir(self._path):
            full_path = os.path.join(self._path, item)

            if os.path.isfile(full_path):
                if item.lower().endswith(self.EXT_WHITELIST):
                    if init:
                        self._documents.append(GMDoc(full_path))
                    else:
                        found = False
                        for doc in self._documents:
                            if doc.path == full_path:
                                found = True

                        if not found:
                            self.documents.append(GMDoc(full_path))

        self.updateState()

        if self._tab_widget is not None:
            self._tab_widget.setTabText(self._tab_index, self.getTabName())

    def onListViewItemActivated(self, model_index):
        doc = model_index.data(Qt.UserRole)
        self._gm.openDocument(doc)
        self.updateState()

    def updateState(self):
        self._open_count = 0
        self._unsaved_count = 0

        model = QStandardItemModel()

        for doc in self._documents:
            item_text = doc.name
            changed = doc.changed()

            if changed:
                item_text = '{}*'.format(item_text)
                self._unsaved_count += 1

            if self._active_document is not None and doc == self._active_document:
                item_text = '> {}'.format(item_text)
                self._open_count += 1
            elif doc.is_open:
                item_text = '+ {}'.format(item_text)
                self._open_count += 1

            item = QStandardItem(item_text)
            item.setData(doc, Qt.UserRole)
            item.setEditable(False)
            model.appendRow(item)

        self._listview.setModel(model)

    def getDocumentByIndex(self, index):
        if 0 <= index < len(self._documents):
            mi = self._listview.model().index(index, 0)
            self._listview.setCurrentIndex(mi)
            return mi.data(Qt.UserRole)
        return None

    def setActiveDocument(self, doc):
        self._active_document = doc
        self.updateState()

    def getPreviousDocument(self):
        previous = None

        if self._active_document is not None:
            for i, doc in enumerate(self._documents):
                if doc == self._active_document:
                    pi = i - 1

                    if pi >= 0:
                        previous = self._documents[pi]

        return previous

    def getNextDocument(self):
        next = None

        if self._active_document is not None:
            for i, doc in enumerate(self._documents):
                if doc == self._active_document:
                    ni = i + 1

                    if ni < len(self._documents):
                        next = self._documents[ni]

        return next

    def getTabName(self):
        return '{} ({})'.format(self._name, len(self._documents))

    def setupTab(self, tab_widget):
        assert isinstance(tab_widget, QTabWidget)

        container = QWidget()
        layout = QVBoxLayout()

        self.updateState()

        layout.addWidget(self._listview)
        container.setLayout(layout)

        tab_widget.addTab(container, self.getTabName())
        self._tab_index = tab_widget.indexOf(container)
        self._tab_widget = tab_widget

    def close(self, active_doc=None):
        for doc in self._documents:
            if active_doc is not None and doc == active_doc:
                continue
            if doc.is_open:
                if not doc.close():
                    return False
        self._closed = True
        return True


class GalleryMark(QMainWindow):

    def __init__(self, l, app, path=None, settings=None):
        super().__init__()
        self.l = l

        self._app = app
        self._app_icon = QIcon(resource_path(APP_ICON))
        self.setWindowIcon(self._app_icon)

        self._settings = settings or QSettings(QSettings.UserScope, APP_ORG, APP_NAME)

        self._explore_path = None
        self._maximize_window = False
        self._window_pos = None
        self._window_size = None

        self._undo_action = None
        self._redo_action = None

        self._active_dir = None
        self._active_doc = None
        self._active_page = None

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._show_welcome_tab = True
        self._welcome_widget = QWidget()
        self._welcome_ui = Ui_WelcomeTab()
        self._welcome_ui.setupUi(self._welcome_widget)
        self._welcome_ui.showWelcomeCheckbox.stateChanged.connect(self.onShowWelcomeTabCheckboxChanged)

        self._status_label = QLabel('v{}'.format(APP_VERSION))
        self.ui.statusbar.addPermanentWidget(self._status_label)

        self.setupEvents()
        self.loadSettings()
        self.updateTheme()

        self.updateDirectoryActions()
        self.updateFileActions()
        self.updateDocumentNavActions()
        self.updateZoomActions()
        self.updateToolSizeText()

        if self._maximize_window:
            self.showMaximized()
        else:
            if self._window_pos is None:
                self.center()
            else:
                self.move(self._window_pos)
            self.resize(self._window_size)
            self.setVisible(True)

        self.setWindowTitle(APP_NAME)

        if path is not None:
            abs_path = os.path.abspath(path)
            if os.path.exists(abs_path):
                if os.path.isdir(abs_path):
                    self.openDirectory(abs_path)
                if os.path.isfile(abs_path):
                    self.openDocument(GMDoc(abs_path))
            else:
                self.l.info('Path passed by argument does not exist, ignoring.')

    def setupEvents(self):
        self.ui.actionDirectoryOpen.triggered.connect(self.onOpenDirectoryTriggered)
        self.ui.actionPreviousFile.triggered.connect(self.onPreviousFileTriggered)
        self.ui.actionNextFile.triggered.connect(self.onNextFileTriggered)
        self.ui.actionSaveOpenFiles.triggered.connect(self.onSaveOpenFilesTriggered)
        self.ui.actionCloseOpenFiles.triggered.connect(self.onCloseOpenFilesTriggered)
        self.ui.actionDirectoryRefresh.triggered.connect(self.onDirectoryRefreshTriggered)
        self.ui.actionShowExplorer.triggered.connect(self.onShowExplorerTriggered)
        self.ui.actionDirectoryClose.triggered.connect(self.onDirectoryCloseTriggered)
        self.ui.actionExit.triggered.connect(self.onExitTriggered)
        self.ui.actionExit.setShortcut(QKeySequence('Alt+F4'))
        self.ui.actionFileOpen.triggered.connect(self.onOpenFileTriggered)
        self.ui.actionFileSave.triggered.connect(self.onFileSaveTriggered)
        self.ui.actionFileClose.triggered.connect(self.onCloseFileTriggered)
        self.ui.actionUndo.triggered.connect(self.onUndoTriggered)
        self.ui.actionRedo.triggered.connect(self.onRedoTriggered)
        self.ui.actionZoomIn.changed.connect(self.onZoomInActionChanged)
        self.ui.actionZoomIn.triggered.connect(self.onZoomInTriggered)
        self.ui.actionZoomOut.changed.connect(self.onZoomOutActionChanged)
        self.ui.actionZoomOut.triggered.connect(self.onZoomOutTriggered)
        self.ui.actionResetView.triggered.connect(self.onResetViewTriggered)
        self.ui.actionPreviousPage.triggered.connect(self.onPreviousPageTriggered)
        self.ui.actionPreviousPage.changed.connect(self.onPreviousPageActionChanged)
        self.ui.actionNextPage.triggered.connect(self.onNextPageTriggered)
        self.ui.actionNextPage.changed.connect(self.onNextPageActionChanged)
        self.ui.actionWelcomeTab.triggered.connect(self.onWelcomeTabTriggered)
        self.ui.actionDarkTheme.changed.connect(self.onThemeActionChanged)

        self.ui.actionAbout.triggered.connect(self.onAboutClicked)

        self.ui.actionPenTool.changed.connect(self.onPenToolChanged)
        self.ui.actionEraserTool.changed.connect(self.onEraserToolChanged)

        self.ui.menuTools.addSeparator()
        decrease_action = self.ui.pageViewer.getDecreaseSizeAction()
        decrease_action.setShortcut(QKeySequence('['))
        decrease_action.triggered.connect(self.updateToolSizeText)
        self.ui.menuTools.addAction(decrease_action)
        increase_action = self.ui.pageViewer.getIncreaseSizeAction()
        increase_action.setShortcut(QKeySequence(']'))
        increase_action.triggered.connect(self.updateToolSizeText)
        self.ui.menuTools.addAction(increase_action)

        self.ui.resetViewBtn.clicked.connect(self.onResetViewBtnClicked)
        self.ui.zoomInBtn.clicked.connect(self.onZoomInBtnClicked)
        self.ui.zoomOutBtn.clicked.connect(self.onZoomOutBtnClicked)
        self.ui.penBtn.clicked.connect(self.onPenBtnClicked)
        self.ui.eraserBtn.clicked.connect(self.onEraserBtnClicked)

        self.ui.prevPageBtn.clicked.connect(self.onPreviousPageBtnClicked)
        self.ui.nextPageBtn.clicked.connect(self.onNextPageBtnClicked)

        self.ui.tabWidget.tabCloseRequested.connect(self.onTabCloseRequested)

        self.ui.pageViewer.mouseRelaseEvent.connect(self.onPageViewerMouseRelease)
        self.ui.pageViewer.wheelZoomEvent.connect(self.onPageViewerWheelZoom)

    def statusMessage(self, message):
        self._status_label.setText(message)

    def tempStatusMessage(self, message, duration=5000):
        self.ui.statusbar.showMessage(message, msecs=duration)

    def loadSettings(self):
        # set window pos and size
        self._window_size = self._settings.value('gmMainWindowSize', defaultValue=self.size())
        self._window_pos = self._settings.value('gmMainWindowPos', defaultValue=None)
        self._maximize_window = self._settings.value('gmMainWindowMaximized', defaultValue=False)

        # set theme
        theme_value = self._settings.value('gmTheme', defaultValue='light')

        if theme_value.lower() == 'dark':
            self.ui.actionDarkTheme.setChecked(True)

        # set initial dir and file explore paths
        self._explore_path = self._settings.value('gmExplorePath', defaultValue=get_download_path())

        # set tool sizes
        self.ui.pageViewer.setPenSize(self._settings.value('gmPenSize', defaultValue=5))
        self.ui.pageViewer.setEraserSize(self._settings.value('gmEraserSize', defaultValue=100))

        # conditionally show welcome tab
        self._show_welcome_tab = self._settings.value('gmShowWelcomeTab', defaultValue=True)

        if self._show_welcome_tab:
            self.showWelcomeTab()

    def saveSettings(self):
        # window pos and size
        self._settings.setValue('gmMainWindowSize', self.size())
        self._settings.setValue('gmMainWindowPos', self.pos())
        self._settings.setValue('gmMainWindowMaximized', int(self.isMaximized()))

        # theme
        self._settings.setValue('gmTheme', 'dark' if self.ui.actionDarkTheme.isChecked() else 'light')

        # initial dir and file explore paths
        self._settings.setValue('gmExplorePath', self._explore_path)

        # save tool sizes
        self._settings.setValue('gmPenSize', self.ui.pageViewer.pen_size)
        self._settings.setValue('gmEraserSize', self.ui.pageViewer.eraser_size)

        # show welcome tab next time
        self._settings.setValue('gmShowWelcomeTab', int(self._show_welcome_tab))

    def showWelcomeTab(self):
        self._welcome_ui.showWelcomeCheckbox.setChecked(self._show_welcome_tab)
        self.ui.tabWidget.addTab(self._welcome_widget, 'Welcome')

    def updateTheme(self):
        if self.ui.actionDarkTheme.isChecked():
            self._app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
        else:
            # I have no idea why, but the pen tool refuses to draw if there isn't
            # at least one stylesheet rule that effects QGraphicsView in any way.
            self._app.setStyleSheet('QGraphicsView { background-color: #CCC; }')

    def updateDirectoryActions(self):
        dir_open = self._active_dir is not None
        self.ui.actionPreviousFile.setEnabled(dir_open and self._active_dir.getPreviousDocument() is not None)
        self.ui.actionNextFile.setEnabled(dir_open and self._active_dir.getNextDocument() is not None)

        if dir_open:
            self._active_dir.updateState()
            self.ui.actionSaveOpenFiles.setEnabled(self._active_dir.unsaved_count > 0)
            self.ui.actionCloseOpenFiles.setEnabled(self._active_dir.open_count > 0)
        else:
            self.ui.actionSaveOpenFiles.setEnabled(False)
            self.ui.actionCloseOpenFiles.setEnabled(False)

        self.ui.actionDirectoryRefresh.setEnabled(dir_open)
        self.ui.actionShowExplorer.setEnabled(dir_open)
        self.ui.actionDirectoryClose.setEnabled(dir_open)

    def updateFileActions(self):
        if self._active_doc is not None and self._active_doc.is_open:
            self.ui.actionFileSave.setEnabled(self._active_doc.changed())
            self.ui.actionFileClose.setEnabled(True)

            if self._active_page is not None:
                self.ui.actionZoomIn.setEnabled(True)
                self.ui.actionZoomOut.setEnabled(True)
                self.ui.actionPenTool.setEnabled(True)
                self.ui.actionEraserTool.setEnabled(True)
            else:
                self.ui.actionZoomIn.setEnabled(False)
                self.ui.actionZoomOut.setEnabled(False)
                self.ui.actionPenTool.setEnabled(False)
                self.ui.actionEraserTool.setEnabled(False)
        else:
            self.ui.actionFileSave.setEnabled(False)
            self.ui.actionFileClose.setEnabled(False)

    def updateEditActions(self):
        if self._active_page is not None:
            self.ui.actionUndo.setEnabled(self._active_page.can_undo)
            self.ui.actionRedo.setEnabled(self._active_page.can_redo)
        else:
            self.ui.actionUndo.setEnabled(False)
            self.ui.actionRedo.setEnabled(False)

    def updateDocumentNavActions(self):
        page_loaded = not self.ui.pageViewer.empty
        prev_enabled = page_loaded and self._active_page.index > 0
        next_enabled = page_loaded and self._active_page.index < self._active_doc.getPageCount() - 1
        self.ui.actionPreviousPage.setEnabled(prev_enabled)
        self.ui.actionNextPage.setEnabled(next_enabled)

    def updateZoomActions(self):
        page_loaded = self._active_page is not None
        self.ui.actionZoomIn.setEnabled(self.ui.pageViewer.canZoomIn() and page_loaded)
        self.ui.actionZoomOut.setEnabled(self.ui.pageViewer.canZoomOut() and page_loaded)

    def updatePageCountLabel(self):
        page_num = 1
        pages = 1

        if self._active_page is not None:
            page_num = self._active_page.index + 1
            pages = self._active_doc.getPageCount()
        else:
            pages = None

        self.ui.pageCountText.setText('Page {} of {}'.format(page_num, pages or '?'))

    def updateToolSizeText(self):
        self.ui.toolSizeText.setText(self.ui.pageViewer.getActiveToolSizeText())

    def openDirectory(self, path):
        self.closeDirectory()

        try:
            self._active_dir = GMDir(self, path)
            self._active_dir.setupTab(self.ui.tabWidget)

            self.ui.tabWidget.setCurrentIndex(self._active_dir.tab_index)

            if len(self._active_dir.documents) > 0:
                if self._active_doc is not None:
                    self.closeDocument()

                doc = self._active_dir.getDocumentByIndex(0)
                self.openDocument(doc)
        except OSError as e:
            msg = 'Failed to open directory "{}": {}'.format(path, str(e))
            self.l.error(msg)
            QErrorMessage(self).showMessage(msg)
            self.tempStatusMessage('Could not open directory "{}".'.format(path))

        self.updateDirectoryActions()
        self.updateFileActions()

    def closeDirectory(self):
        if self._active_dir is not None:
            self.ui.tabWidget.tabCloseRequested.emit(self._active_dir.tab_index)

    def saveCopy(self):
        file_name = self._active_doc.getSaveFilename()

        try:
            self._active_doc.saveDrawingPDF()
            file_size = get_file_size(self._active_doc.getSavePath())
            self.l.info('Saved copy "{}" from "{}".'.format(file_name, self._active_doc.path))
            self.tempStatusMessage('Saved copy as "{}" ({})'.format(file_name, format_file_size(file_size)))
        except RuntimeError as e:
            msg = 'Failed to save "{}": {}'.format(file_name, str(e))
            self.l.error(msg)
            QErrorMessage(self).showMessage(msg)

        if self._active_dir is not None:
            self._active_dir.refresh()

    def loadPage(self, index):
        result = self._active_doc.getPage(index)

        if result is None:
            self.tempStatusMessage('Failed to get page {}.'.format(index))
        else:
            self._active_page = result
            self.onPageLoaded()

    def openDocument(self, doc):
        assert isinstance(doc, GMDoc)

        self._active_doc = doc

        try:
            self._active_doc.open()

            if self._active_dir is not None:
                if self._active_doc in self._active_dir.documents:
                    self._active_dir.setActiveDocument(self._active_doc)

            self.onDocumentOpened()
        except RuntimeError as e:
            msg = 'Failed to open "{}": {}'.format(doc.name, str(e))
            self.l.error(msg)
            QErrorMessage(self).showMessage(msg)
            self.tempStatusMessage('Could not open "{}".'.format(doc.name))

            if self._active_dir is not None:
                self._active_dir.refresh()

    def closeDocument(self):
        if self._active_doc is not None:
            if self._active_doc.close():
                self.ui.pageViewer.reset()

                msg = 'Closed "{}".'.format(self._active_doc.name)
                self.l.info(msg)
                self.tempStatusMessage(msg)

                self._active_page = None
                self._active_doc = None

                if self._active_dir is not None:
                    self._active_dir.setActiveDocument(None)

                self.onDocumentClosed()
            else:
                self.tempStatusMessage('User canceled document close.')

    def onAboutClicked(self):
        dialog = QDialog(self)
        ui = Ui_About(self._app_icon, APP_NAME, APP_VERSION, APP_WEBSITE)
        ui.setupUi(dialog)
        dialog.exec()

    def onShowWelcomeTabCheckboxChanged(self, state):
        self._show_welcome_tab = state

    def onWelcomeTabTriggered(self):
        self.showWelcomeTab()

    def onThemeActionChanged(self):
        self.updateTheme()

    def onPageViewerMouseRelease(self):
        self.updateDirectoryActions()
        self.updateFileActions()
        self.updateEditActions()

    def onPageViewerWheelZoom(self):
        self.updateZoomActions()

    def onPreviousFileTriggered(self):
        if self._active_dir is not None:
            doc = self._active_dir.getPreviousDocument()

            if doc is not None:
                self.openDocument(doc)

        self.updateDirectoryActions()

    def onNextFileTriggered(self):
        if self._active_dir is not None:
            doc = self._active_dir.getNextDocument()

            if doc is not None:
                self.openDocument(doc)

        self.updateDirectoryActions()

    def onSaveOpenFilesTriggered(self):
        if self._active_dir is not None:
            for doc in self._active_dir.documents:
                if doc.is_open and doc.changed():
                    doc.saveDrawingPDF()

            self._active_dir.refresh()

        self.updateDirectoryActions()

    def onCloseOpenFilesTriggered(self):
        if self._active_dir is not None:
            for doc in self._active_dir.documents:
                if doc == self._active_doc:
                    if not self.closeDocument():
                        break
                else:
                    if doc.is_open:
                        if not doc.close():
                            break

            self._active_dir.refresh()

        self.updateDirectoryActions()

    def onShowExplorerTriggered(self):
        if self._active_dir is not None:
            webbrowser.open(self._active_dir.path)

    def onUndoTriggered(self):
        if self._active_page is not None:
            self._active_page.undo()

        self.updateDirectoryActions()
        self.updateFileActions()
        self.updateEditActions()

    def onRedoTriggered(self):
        if self._active_page is not None:
            self._active_page.redo()

        self.updateDirectoryActions()
        self.updateFileActions()
        self.updateEditActions()

    def onZoomInActionChanged(self):
        self.ui.zoomInBtn.setEnabled(self.ui.actionZoomIn.isEnabled())

    def onZoomOutActionChanged(self):
        self.ui.zoomOutBtn.setEnabled(self.ui.actionZoomOut.isEnabled())

    def onPreviousPageActionChanged(self):
        self.ui.prevPageBtn.setEnabled(self.ui.actionPreviousPage.isEnabled())

    def onNextPageActionChanged(self):
        self.ui.nextPageBtn.setEnabled(self.ui.actionNextPage.isEnabled())

    def onPenToolChanged(self):
        checked = self.ui.actionPenTool.isChecked()

        if checked:
            self.ui.actionEraserTool.setChecked(False)
            self.ui.pageViewer.setToolMode(ToolMode.PEN)
        else:
            self.ui.pageViewer.setToolMode(ToolMode.NOTHING)

        self.ui.penBtn.setEnabled(self.ui.actionPenTool.isEnabled())
        self.ui.penBtn.setChecked(checked)
        self.updateToolSizeText()

    def onEraserToolChanged(self):
        checked = self.ui.actionEraserTool.isChecked()

        if checked:
            self.ui.actionPenTool.setChecked(False)
            self.ui.pageViewer.setToolMode(ToolMode.ERASER)
        else:
            self.ui.pageViewer.setToolMode(ToolMode.NOTHING)

        self.ui.eraserBtn.setEnabled(self.ui.actionEraserTool.isEnabled())
        self.ui.eraserBtn.setChecked(checked)
        self.updateToolSizeText()

    def onTabCloseRequested(self, i):
        if self._active_dir is not None and i == self._active_dir.tab_index:
            if self._active_dir.close(active_doc=self._active_doc):
                msg = 'Closed directory "{}".'.format(self._active_dir.path)
                self.l.info(msg)
                self.tempStatusMessage(msg)

                self.ui.tabWidget.removeTab(i)

                self._active_dir = None
                self.updateDirectoryActions()
                self.updateFileActions()
            else:
                self.tempStatusMessage('User canceled closing directory.')
        else:
            self.ui.tabWidget.removeTab(i)

    def onOpenDirectoryTriggered(self):
        path = QFileDialog.getExistingDirectory(self, 'Open directory', self._explore_path)

        if path and path is not '':
            if os.path.exists(path):
                self._explore_path = path
                self.openDirectory(path)
            else:
                self.l.info('open directory: "{}" does not exist, ignoring.'.format(path))
        else:
            self.l.info('open directory: path is empty, ignoring.')

    def onDirectoryRefreshTriggered(self):
        if self._active_dir is not None:
            self._active_dir.refresh()

    def onDirectoryCloseTriggered(self):
        self.closeDirectory()

    def onOpenFileTriggered(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Open file', self._explore_path, '*.pdf')

        if path and path is not '':
            if os.path.exists(path):
                self._explore_path = path
                self.openDocument(GMDoc(path))
            else:
                self.l.info('open file: "{}" does not exist, ignoring.'.format(path))
        else:
            self.l.info('open file: path is empty, ignoring.')

    def onFileSaveTriggered(self):
        self.saveCopy()

    def onCloseFileTriggered(self):
        self.closeDocument()

    def onResetViewTriggered(self):
        self.ui.pageViewer.fitPage()
        self.updateZoomActions()

    def onResetViewBtnClicked(self):
        self.ui.actionResetView.trigger()

    def onZoomInChanged(self):
        self.ui.actionZoomIn.setEnabled(self.ui.actionZoomIn.isEnabled())

    def onZoomInTriggered(self):
        self.ui.pageViewer.zoomIn()
        self.updateZoomActions()

    def onZoomOutChanged(self):
        self.ui.actionZoomOut.setEnabled(self.ui.actionZoomOut.isEnabled())

    def onZoomOutTriggered(self):
        self.ui.pageViewer.zoomOut()
        self.updateZoomActions()

    def onZoomInBtnClicked(self):
        self.ui.actionZoomIn.trigger()

    def onZoomOutBtnClicked(self):
        self.ui.actionZoomOut.trigger()

    def onPenBtnClicked(self):
        self.ui.actionPenTool.toggle()

    def onEraserBtnClicked(self):
        self.ui.actionEraserTool.toggle()

    def onPreviousPageTriggered(self):
        if self._active_page is not None:
            index = self._active_page.index - 1
            if index >= 0:
                self.loadPage(index)
        self.updateDocumentNavActions()

    def onPreviousPageBtnClicked(self):
        self.ui.actionPreviousPage.trigger()

    def onNextPageTriggered(self):
        if self._active_page is not None:
            index = self._active_page.index + 1
            if index < self._active_doc.getPageCount():
                self.loadPage(index)
        self.updateDocumentNavActions()

    def onNextPageBtnClicked(self):
        self.ui.actionNextPage.trigger()

    def onPageLoaded(self):
        self.ui.pageViewer.setPage(self._active_page)

        self.updateFileActions()
        self.updatePageCountLabel()
        self.updateDocumentNavActions()

    def onDocumentOpened(self):
        file_size = get_file_size(self._active_doc.path)
        file_name = self._active_doc.name
        self.l.info('Opened "{}".'.format(file_name))
        self.tempStatusMessage('Opened "{}" ({})'.format(file_name, format_file_size(file_size)))
        self.updateDirectoryActions()
        self.updateFileActions()
        self.updateEditActions()
        self.loadPage(0)

    def onDocumentClosed(self):
        self.updateFileActions()
        self.updateEditActions()
        self.updateDocumentNavActions()
        self.updateZoomActions()
        self.updatePageCountLabel()

    def onExitTriggered(self):
        QCoreApplication.quit()

    def closeEvent(self, event):
        if self._active_dir is not None:
            for doc in self._active_dir.documents:
                if doc.is_open:
                    if not doc.close():
                        event.ignore()
                        return

        if self._active_doc is not None and self._active_doc.is_open:
            self._active_doc.close()

        self.saveSettings()
        event.accept()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonRelease:
            if event.button() == Qt.LeftButton:
                if self._active_dir is not None:
                    self._active_dir.updateState()

        return False

    def center(self):
        g = self.frameGeometry()
        g.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(g.topLeft())


if __name__ == '__main__':
    log = logging.getLogger(APP_NAME)
    log_stdo = logging.StreamHandler()

    log_stdo.setLevel(logging.DEBUG)
    log_stdo.setFormatter(logging.Formatter('[%(levelname)s][%(funcName)s]: %(message)s'))
    log.addHandler(log_stdo)

    QCoreApplication.setApplicationName(APP_NAME)
    QCoreApplication.setApplicationVersion(APP_VERSION)
    QCoreApplication.setOrganizationName(APP_ORG)

    ap = argparse.ArgumentParser(description=APP_NAME)
    ap.add_argument('--reset', action='store_true', dest='reset',
                    help='Reset user preferences and start.')
    ap.add_argument(nargs='?', type=str, dest='path', default=None,
                    help='Path of a file or directory to open on startup.')

    args = ap.parse_args()
    reset = args.reset
    path = args.path

    qa = QApplication(sys.argv)

    s = None
    if reset:
        s = QSettings(QSettings.UserScope, APP_ORG, APP_NAME)
        s.clear()

    main_window = GalleryMark(log, qa, path=path, settings=s)

    sys.exit(qa.exec_())
