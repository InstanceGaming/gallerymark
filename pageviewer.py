from PyQt5.QtCore import Qt, pyqtSignal, QRectF
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush
from PyQt5.QtWidgets import (QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsEllipseItem, QAction)

from gallerymark import ToolMode, DrawCommand
from utils import copyPixmap


class PageViewer(QGraphicsView):
    mouseRelaseEvent = pyqtSignal()
    wheelZoomEvent = pyqtSignal()

    @property
    def drawing(self):
        return self._drawing

    @property
    def tool_mode(self):
        return self._toolMode

    @property
    def empty(self):
        return self._page is None

    @property
    def page_layer(self):
        return self._pageLayer

    @property
    def drawing_layer(self):
        return self._drawingLayer

    @property
    def page(self):
        return self._page

    @property
    def pen_size(self):
        return self._pen.width()

    @property
    def eraser_size(self):
        return self._eraserSize

    def __init__(self, parent):
        super(PageViewer, self).__init__(parent)

        self._page = None

        # todo: add all these constants to preferences dialog
        self._zoom = 0
        self._zoomMaxDistance = 10
        self._zoomInFactor = 1.25
        self._zoomOutFactor = 0.8
        self._panDivisor = 2
        self._toolMode = ToolMode.NOTHING
        self._previousToolModeDrag = ToolMode.NOTHING
        self._drawing = False
        self._dragStart = None
        self._drawPoint = None
        self._lastPenPos = None

        self._scene = QGraphicsScene(self)
        self._pageLayer = None
        self._drawingLayer = None

        self._predrawPixmap = None

        self._eraserSize = 100
        self._eraserEllipse = self.getEraserEllipse()

        pen_brush = QBrush(QColor('red'), Qt.SolidPattern)
        self._pen = QPen(pen_brush, 5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)

        self._increaseSizeAction = QAction('Increase tool size', self)
        self._increaseSizeAction.setEnabled(False)
        self._increaseSizeAction.triggered.connect(self.onIncreaseSizeActionTriggered)

        self._decreaseSizeAction = QAction('Decrease tool size', self)
        self._decreaseSizeAction.setEnabled(False)
        self._decreaseSizeAction.triggered.connect(self.onDecreaseSizeActionTriggered)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setMouseTracking(True)

    def reset(self):
        self.setInteractive(False)
        self.setToolMode(ToolMode.NOTHING)
        self.setScene(QGraphicsScene(self))

        self._page = None
        self._zoom = 0

    def getEraserEllipse(self):
        brush = QBrush(QColor(0, 0, 0, alpha=64), Qt.SolidPattern)
        pen = QPen(brush, 2, Qt.DashDotLine, Qt.RoundCap, Qt.RoundJoin)
        pen.setCosmetic(True)
        ellipse = QGraphicsEllipseItem(0, 0, self._eraserSize, self._eraserSize)
        ellipse.setPen(pen)
        return ellipse

    def fitPage(self):
        if not self.empty:
            rect = QRectF(self._pageLayer.pixmap().rect())
            if not rect.isNull():
                self.setSceneRect(rect)
                unity = self.transform().mapRect(QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.scale(factor, factor)
                self._zoom = 0

    def setPage(self, page):
        self._page = page

        if not self._page.page_image.isNull():
            self._scene.clear()

            self._pageLayer = QGraphicsPixmapItem(self._page.page_image)
            self._scene.addItem(self._pageLayer)
            self._drawingLayer = QGraphicsPixmapItem(self._page.drawing_image)
            self._scene.addItem(self._drawingLayer)

            self.fitPage()
            self._eraserEllipse = self.getEraserEllipse()
            self.setScene(self._scene)
            self.setToolMode(self._toolMode)
            self.setInteractive(True)

    def canZoomIn(self):
        return self._zoom < self._zoomMaxDistance

    def canZoomOut(self):
        return self._zoom > 0

    def zoomIn(self):
        if self.canZoomIn():
            self._zoom += 1
            self._applyZoom(self._zoomInFactor)
            return True
        return False

    def zoomOut(self):
        if self.canZoomOut():
            self._zoom -= 1
            self._applyZoom(self._zoomOutFactor)
            return True
        return False

    def _applyZoom(self, factor):
        if self._zoom > 0:
            self.scale(factor, factor)
        else:
            self._zoom = 0
            self.fitPage()

    def wheelEvent(self, event):
        if not self.empty:
            if event.angleDelta().y() > 0:
                factor = self._zoomInFactor
                if not self.zoomIn():
                    return
            else:
                factor = self._zoomOutFactor
                self.zoomOut()

            self._applyZoom(factor)
            self.wheelZoomEvent.emit()

    def _penDraw(self, pos):
        self._drawing = True
        self._lastPenPos = self._drawPoint
        self._drawPoint = pos
        self.update()

    def _eraseDraw(self, pos):
        self._drawing = True
        self._drawPoint = pos
        self.update()

    def mousePressEvent(self, event):
        if not self.empty:
            button = event.button()
            scenePos = self.mapToScene(event.pos())

            if button == Qt.MiddleButton:
                self._previousToolModeDrag = self._toolMode
                self.setToolMode(ToolMode.DRAGGING)
                self._dragStart = scenePos
            elif button == Qt.LeftButton:
                if self._toolMode == ToolMode.NOTHING:
                    self.setToolMode(ToolMode.DRAGGING)
                else:
                    sceneRect = self._drawingLayer.mapRectToScene(QRectF(self._page.drawing_image.rect()))

                    if sceneRect.contains(scenePos.x(), scenePos.y()):
                        self._predrawPixmap = copyPixmap(self._page.drawing_image)
                        if self._toolMode == ToolMode.PEN:
                            self._penDraw(scenePos)
                        if self._toolMode == ToolMode.ERASER:
                            self._eraseDraw(scenePos)

        super(PageViewer, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        scenePos = self.mapToScene(event.pos())

        if self._toolMode == ToolMode.ERASER:
            r = self._eraserEllipse.rect()
            x = scenePos.x() - (r.width() / 2)
            y = scenePos.y() - (r.height() / 2)
            self._eraserEllipse.setPos(x, y)

        if not self.empty:
            if self._toolMode == ToolMode.DRAGGING and self._dragStart is not None:
                delta = self.mapToScene(event.pos())
                self.translate(delta.x() - self._dragStart.x(), delta.y() - self._dragStart.y())
            else:
                if self._drawing:
                    if self._toolMode == ToolMode.PEN:
                        self._penDraw(scenePos)

        super(PageViewer, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if not self.empty:
            button = event.button()
            scenePos = self.mapToScene(event.pos())

            if button == Qt.MiddleButton:
                self.setToolMode(self._previousToolModeDrag)
            elif button == Qt.LeftButton:
                if self._toolMode == ToolMode.DRAGGING:
                    self.setToolMode(ToolMode.NOTHING)
                elif self._toolMode == ToolMode.PEN:
                    self._penDraw(scenePos)
                    self._page.pushCommand(DrawCommand(self, self._predrawPixmap))
                    self._lastPenPos = None
                elif self._toolMode == ToolMode.ERASER:
                    self._eraseDraw(scenePos)
                    self._page.pushCommand(DrawCommand(self, self._predrawPixmap))

                self._drawPoint = None
                self._drawing = False

        self.mouseRelaseEvent.emit()

    def paintEvent(self, event):
        if self._drawing:
            painter = QPainter(self._page.drawing_image)
            painter.setRenderHint(QPainter.HighQualityAntialiasing, True)

            if self._toolMode == ToolMode.ERASER:
                painter.setPen(Qt.NoPen)
                painter.setBrush(painter.background())

                r = int(self._eraserSize / 2)
                painter.drawEllipse(self._drawPoint, r, r)

            if self._toolMode == ToolMode.PEN:
                painter.setPen(self._pen)

                if self._lastPenPos is None:
                    painter.drawPoint(self._drawPoint)
                else:
                    painter.drawLine(self._lastPenPos, self._drawPoint)

            painter.end()
            self.updateDrawingLayer()

        super(PageViewer, self).paintEvent(event)

    def setToolMode(self, mode: ToolMode):
        self._toolMode = mode

        self._increaseSizeAction.setEnabled(False)
        self._decreaseSizeAction.setEnabled(False)

        for item in self._scene.items():
            if isinstance(item, QGraphicsEllipseItem):
                self._scene.removeItem(item)

        if self._toolMode == ToolMode.DRAGGING:
            self.setCursor(Qt.ClosedHandCursor)
        else:
            if self._toolMode == ToolMode.ERASER:
                self._scene.addItem(self._eraserEllipse)

                self._increaseSizeAction.setText('Increase Eraser width')
                self._decreaseSizeAction.setText('Decrease Eraser width')
                self._increaseSizeAction.setEnabled(True)
                self._decreaseSizeAction.setEnabled(True)
            elif self._toolMode == ToolMode.PEN:
                self.setDragMode(QGraphicsView.NoDrag)
                self.setCursor(Qt.CrossCursor)

                self._increaseSizeAction.setText('Increase Pen width')
                self._decreaseSizeAction.setText('Decrease Pen width')
                self._increaseSizeAction.setEnabled(True)
                self._decreaseSizeAction.setEnabled(True)
            else:
                self.setDragMode(QGraphicsView.NoDrag)
                self.setCursor(Qt.ArrowCursor)

    def setEraserSize(self, v):
        if 500 >= v >= 10:
            self._eraserEllipse.setRect(0, 0, v, v)
            self._eraserSize = v

    def setPenSize(self, v):
        if 30 >= v > 0:
            self._pen.setWidth(v)

    def onIncreaseSizeActionTriggered(self):
        if self._toolMode == ToolMode.ERASER:
            v = self._eraserSize + 1
            self.setEraserSize(v)
        elif self._toolMode == ToolMode.PEN:
            v = self._pen.width() + 1
            self.setPenSize(v)

    def onDecreaseSizeActionTriggered(self):
        if self._toolMode == ToolMode.ERASER:
            v = self._eraserSize - 1
            self.setEraserSize(v)
        elif self._toolMode == ToolMode.PEN:
            v = self._pen.width() - 1
            self.setPenSize(v)

    def getActiveToolSizeText(self):
        if self._toolMode == ToolMode.ERASER:
            return '{:03d}px'.format(self._eraserSize)
        elif self._toolMode == ToolMode.PEN:
            return '{:02d}px'.format(self._pen.width())
        else:
            return ''

    def getIncreaseSizeAction(self):
        return self._increaseSizeAction

    def getDecreaseSizeAction(self):
        return self._decreaseSizeAction

    def updateDrawingLayer(self):
        self._drawingLayer.setPixmap(self._page.drawing_image)
