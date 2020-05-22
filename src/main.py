#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, os, numpy, PIL, csv
from PySide2 import QtCore, QtGui, QtWidgets
from PIL import Image, ImagePalette, ImageQt, ImageSequence
from abc import ABCMeta, abstractmethod
from drawtools import *

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setAcceptDrops(True)
        self.setWindowTitle("pixpeer")
        self.widget = Widget(self)
        self.setCentralWidget(self.widget)
        globals()['Window'] = self
#        drawtools.globals()['Window'] = self
        self.__create_menu()
        self.show()
    def __create_menu(self):
        self.menus = {}
        self.menus['File'] = QtWidgets.QMenu('File', self)
        self.menus['Draw'] = QtWidgets.QMenu('Draw', self)
        self.menus['Animation'] = QtWidgets.QMenu('Animation', self)
        self.__create_actions()
        for key in self.menus.keys():
            self.menuBar().addMenu(self.menus[key])
    def __create_actions(self):
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'res', 'actions.tsv'), 'r') as f:
            header = next(csv.reader(f, delimiter='\t')) # 先頭行をヘッダ行として飛ばす
            rows = csv.reader(f, delimiter='\t')
            for row in rows:
#                print(row[1], row[2], row[9], row[5])
                self.menus[row[0]].addAction(ActionCreator.create(row[1], row[2], row[9], row[5]))
    def mousePressEvent(self, event):
        super(self.__class__, self).mousePressEvent(event)
        self.widget.update()
    def mouseMoveEvent(self, event):
        super(self.__class__, self).mouseMoveEvent(event)
        self.widget.update()
    def mouseReleaseEvent(self, event):
        super(self.__class__, self).mouseReleaseEvent(event)
        self.widget.update()
    def dragEnterEvent(self, event):
        super(self.__class__, self).dragEnterEvent(event)
        self.widget.update()
    def dragMoveEvent(self, event):
        super(self.__class__, self).dragMoveEvent(event)
        self.widget.update()
    def dropEvent(self, event):
        super(self.__class__, self).dropEvent(event)
        self.widget.update()

class Widget(QtWidgets.QWidget):
    def __init__(self, parent):
        super(self.__class__, self).__init__(parent)
        self.setAcceptDrops(True)
        self.view = GraphicView()
        globals()['GraphicView'] = self.view

        self.animation = AnimationWidget()
#        self.animation.setMinimumHeight(self.animation.height())
#        self.animation.setMaximumHeight(self.animation.height()*1.2)
        self.animation.setMinimumHeight(32)
        self.animation.setMaximumHeight(64)
        self.animation.resize(self.animation.width(), self.animation.height())
        globals()['AnimationWidget'] = self.animation

        self.drawtoolbox = DrawToolbox()

        scroller1 = QtWidgets.QScrollArea()
        scroller1.setWidget(self.view)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.animation, 0, 0)
        layout.addWidget(scroller1, 1, 0)
        layout.addWidget(self.drawtoolbox, 2, 0)

        self.setLayout(layout)
        self.resize(self.view.width(), self.view.height())
        self.show()
    @property
    def GraphicsView(self): return self.view
    def mousePressEvent(self, event):
        super(self.__class__, self).mousePressEvent(event)
        self.view.scene().update()
        self.view.update()
#        self.animation.mousePressEvent(event)
#        self.animation.update()
    def mouseMoveEvent(self, event):
        super(self.__class__, self).mouseMoveEvent(event)
        self.view.scene().update()
        self.view.update()
#        self.animation.mouseMoveEvent(event)
#        self.animation.update()
    def mouseReleaseEvent(self, event):
        super(self.__class__, self).mouseReleaseEvent(event)
        self.view.scene().update()
        self.view.update()
#        self.animation.mouseReleaseEvent(event)
#        self.animation.update()
    def dragEnterEvent(self, event):
        super(self.__class__, self).dragEnterEvent(event)
        self.view.dragEnterEvent(event)
        self.view.scene().update()
        self.view.update()
#        self.animation.dragEnterEvent(event)
#        self.animation.update()
    def dragMoveEvent(self, event):
        super(self.__class__, self).dragMoveEvent(event)
        self.view.scene().update()
        self.view.update()
#        self.animation.dragMoveEvent(event)
#        self.animation.update()
    def dropEvent(self, event):
        super(self.__class__, self).dropEvent(event)
        self.view.scene().update()
        self.view.update()
        self.animation.dropEvent(event)
#        self.animation.update()

class GraphicView(QtWidgets.QGraphicsView):
    def __init__(self):
        QtWidgets.QGraphicsView.__init__(self)
        self.setAcceptDrops(True)
        self.__editorScene = EditorScene(self)
        self.setScene(self.__editorScene)
#        globals()['EditorScene'] = self.__editorScene
    def mousePressEvent(self, event):
        super(self.__class__, self).mousePressEvent(event)
        self.scene().update()
    def mouseMoveEvent(self, event):
        super(self.__class__, self).mouseMoveEvent(event)
        self.scene().update()
    def mouseReleaseEvent(self, event):
        super(self.__class__, self).mouseReleaseEvent(event)
        self.scene().update()
    @property
    def Scene(self): return self.__editorScene
    def dragEnterEvent(self, event):
        super(self.__class__, self).dragEnterEvent(event)
        self.scene().update()
    def dragEnterEvent(self, event):
        super(self.__class__, self).dragMoveEvent(event)
        self.scene().update()
    def dropEvent(self, event):
        super(self.__class__, self).dropEvent(event)
        self.scene().update()

class EditorScene(QtWidgets.QGraphicsScene):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.size = 16
        self.scale = 32
        self.setSceneRect(0, 0, self.size*self.scale, self.size*self.scale)

        self.selected = PixelSelectedItem()
        self.addItem(self.selected)

        self.grid = GridItem()
        self.addItem(self.grid)

        self.background = BackgroundItem()
        self.addItem(self.background)

        self.editable = EditableItem()
        self.addItem(self.editable)

        self.drawable = DrawableItem()
        self.addItem(self.drawable)

        self.background.setZValue(0)
        self.drawable.setZValue(1)
        self.editable.setZValue(2)
        self.grid.setZValue(9998)
        self.selected.setZValue(9999)

        # Frame側でも使いたいので
        globals()['Drawable'] = self.drawable

    def mousePressEvent(self, event):
        for item in self.items():
            item.mousePressEvent(event)
        super(self.__class__, self).mousePressEvent(event)
    def mouseMoveEvent(self, event):
        for item in self.items():
            item.setAcceptHoverEvents(True)
            item.mouseMoveEvent(event)
        super(self.__class__, self).mouseMoveEvent(event)
    def mouseReleaseEvent(self, event):
        for item in self.items():
            item.mouseReleaseEvent(event)
        super(self.__class__, self).mousePressEvent(event)
    def dragEnterEvent(self, event):
        for item in self.items():
            item.setAcceptDrops(True)
            if event is type(QtWidgets.QGraphicsSceneDragDropEvent):
                item.dragEnterEvent(event)
        if event is type(QtWidgets.QGraphicsSceneDragDropEvent):
            super(self.__class__, self).dragEnterEvent(event)
    def dragMoveEvent(self, event):
        for item in self.items():
            item.setAcceptDrops(True)
            if event is type(QtWidgets.QGraphicsSceneDragDropEvent):
                item.dragEnterEvent(event)
        if event is type(QtWidgets.QGraphicsSceneDragDropEvent):
            super(self.__class__, self).dragEnterEvent(event)
    def dropEvent(self, event):
        for item in self.items():
            item.setAcceptDrops(True)
            item.dropEvent(event)
        if event is type(QtWidgets.QGraphicsSceneDragDropEvent):
            super(self.__class__, self).dropEvent(event)
    @property
    def Selected(self): return self.selected
    @property
    def Grid(self): return self.grid
    @property
    def Background(self): return self.background
    @property
    def Drawable(self): return self.drawable
    @property
    def Editable(self): return self.editable

class EditableItem(QtWidgets.QGraphicsRectItem):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.scale = 32
#        img = QtGui.QImage(self.pixmap.width(), self.pixmap.height(), QtGui.QImage.Format_ARGB32)
        img = QtGui.QImage(16, 16, QtGui.QImage.Format_ARGB32)
        img.fill(QtGui.QColor(0,0,0,0))
        self.pixmap = QtGui.QPixmap.fromImage(img)
    def paint(self, painter, option, widget):
        painter.drawPixmap(0, 0, self.pixmap.width()*self.scale, self.pixmap.height()*self.scale, self.pixmap)
    def clear(self):
        painter = QtGui.QPainter(self.pixmap)
        painter.setBrush(QtCore.Qt.transparent)
        painter.setPen(QtCore.Qt.transparent)
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_Source)
        painter.fillRect(self.pixmap.rect(), QtCore.Qt.transparent)
        painter.end()
    @property
    def Pixmap(self): return self.pixmap

class DrawableItem(QtWidgets.QGraphicsRectItem):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        self.setAcceptHoverEvents(True)
        self.scale = 32
        self.pixels = Pixels()
        self.actions = {}
        img = QtGui.QImage(self.pixels.Width, self.pixels.Height, QtGui.QImage.Format_ARGB32)
        img.fill(QtGui.QColor(0,0,0,0))
        self.pixmap = QtGui.QPixmap.fromImage(img)
        self.__selected = (0, 0)
        self.__draw_tools = {}
#        self.__draw_tools['Select'] = SelectRectangleTool()
        self.__draw_tools['Pen'] = PenTool()
        self.__draw_tools['Line'] = LineTool()
        self.__draw_tools['Bucket'] = BucketTool()
        self.__draw_tools['Rectangle'] = RectangleTool()
        self.__draw_tools['Ellipse'] = EllipseTool()
        self.__draw_tool = self.__draw_tools['Pen']
    @property
    def DrawTool(self): return self.__draw_tool
    @property
    def DrawTools(self): return self.__draw_tools
    @DrawTool.setter
    def DrawTool(self, value):
        if isinstance(value, DrawTool): self.__draw_tool = value
    def selectedDrawTool(self, name):
        self.DrawTool = self.DrawTools[name]
    def paint(self, painter, option, widget):
        painter.drawPixmap(0, 0, self.pixels.Width*self.scale, self.pixels.Height*self.scale, self.pixmap)
    def mouseMoveEvent(self, event):
        pos = event.scenePos()
        x = int(pos.x()//self.scale)
        y = int(pos.y()//self.scale)
        x = max(0, x)
        y = max(0, y)
        x = min(x, self.pixels.Width-1)
        y = min(y, self.pixels.Height-1)
        if event.buttons() & QtCore.Qt.LeftButton:
            GraphicView.Scene.Editable.clear()
            self.__draw_tool.editing(x, y, GraphicView.Scene.Editable.Pixmap)
            self.__update_frame_list(event)
        if event.buttons() & QtCore.Qt.RightButton:
            GraphicView.Scene.Editable.clear()
            self.__draw_tool.editing(x, y, GraphicView.Scene.Editable.Pixmap)
            self.__update_frame_list(event)

    def mousePressEvent(self, event):
        pos = event.scenePos()
        x = int(pos.x()//self.scale)
        y = int(pos.y()//self.scale)
        x = max(0, x)
        y = max(0, y)
        x = min(x, self.pixels.Width-1)
        y = min(y, self.pixels.Height-1)
        if event.buttons() & QtCore.Qt.LeftButton:
            self.__draw_tool.Color = QtGui.QColor(255,0,0,255)
            self.__draw_tool.EditingColor = QtGui.QColor(255,0,0,96)
            self.__draw_tool.begin(x, y, GraphicView.Scene.Editable.Pixmap)
            self.__draw_tool.editing(x, y, GraphicView.Scene.Editable.Pixmap)
            self.__update_frame_list(event)
        if event.buttons() & QtCore.Qt.RightButton:
            self.__draw_tool.EditingColor = QtGui.QColor(0,0,0,0)
            self.__draw_tool.Color = QtGui.QColor(0,0,0,0)
            self.__draw_tool.begin(x, y, GraphicView.Scene.Editable.Pixmap)
            self.__draw_tool.editing(x, y, GraphicView.Scene.Editable.Pixmap)
            self.__update_frame_list(event)

    def mouseReleaseEvent(self, event):
        pos = event.scenePos()
        x = int(pos.x()//self.scale)
        y = int(pos.y()//self.scale)
        x = max(0, x)
        y = max(0, y)
        x = min(x, self.pixels.Width-1)
        y = min(y, self.pixels.Height-1)
        self.__draw_tool.end(x, y, self.pixmap)
        GraphicView.Scene.Editable.clear()
        self.__update_frame_list(event)

    def __update_frame_list(self, event):
        for idx in FrameListView.selectedIndexes():
            FrameListView.Model.update_pixmap(idx, self.pixmap)
            FrameListView.setCurrentIndex(FrameListView.Model.index(idx.row(),0))
        FrameListView.viewport().update()

    def mouseDoubleClickEvent(self, event):
        pass
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_name = url.toLocalFile()
            print("Dropped file: " + file_name)
            self.Pixels.load(file_name)
    @property
    def Pixels(self): return self.pixels
    @Pixels.setter
    def Pixels(self, value):
        for y in range(value.Height):
            for x in range(value.Width):
                self.pixels.Pixels[y][x] = value.Pixels[y][x]
    @property
    def Pixmap(self): return self.pixmap
    @Pixmap.setter
    def Pixmap(self, value):
        if isinstance(value, QtGui.QPixmap): self.pixmap = value


class BackgroundItem(QtWidgets.QGraphicsRectItem):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.size = 16
        self.scale = 32
        self.colors = [QtGui.QColor(196,196,196,255), QtGui.QColor(232,232,232,255)]
    def paint(self, painter, option, widget):
        for i in range(self.size*self.size):
            x = (i % self.size)
            y = (i // self.size)
            color = QtGui.QColor(128,128,128,255) if 0 == (i % 2) and 0 == (x % 2) else QtGui.QColor(196,196,196,255)
            painter.fillRect(x * (self.scale),               y * (self.scale),               self.scale//2, self.scale//2, self.colors[0])
            painter.fillRect(x * (self.scale)+self.scale//2, y * (self.scale)+self.scale//2, self.scale//2, self.scale//2, self.colors[0])
            painter.fillRect(x * (self.scale)+self.scale//2, y * (self.scale),               self.scale//2, self.scale//2, self.colors[1])
            painter.fillRect(x * (self.scale),               y * (self.scale)+self.scale//2, self.scale//2, self.scale//2, self.colors[1])

class GridItem(QtWidgets.QGraphicsRectItem):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.size = 16
        self.scale = 32
    def paint(self, painter, option, widget):
        painter.fillRect(widget.rect(), QtGui.QBrush(QtGui.QColor(0,0,0,0), QtCore.Qt.SolidPattern))
        lines = []
        for y in range(self.size+1):
            lines.append(QtCore.QLine(0, y*self.scale, self.size*self.scale, y*self.scale))
        for x in range(self.size+1):
            lines.append(QtCore.QLine(x*self.scale, 0, x*self.scale, self.size*self.scale))
        painter.drawLines(lines)

class PixelSelectedItem(QtWidgets.QGraphicsRectItem):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.width = 16
        self.height = 16
        self.scale = 32
        self.__pen = QtGui.QPen(QtGui.QColor(0,255,0), 1, QtCore.Qt.DashLine)
        self.__selected = [0, 0]
        self.__draw_color = QtGui.QColor(255,0,0)
    def paint(self, painter, option, widget):
        painter.setPen(self.__pen)
        painter.drawRect(self.__selected[0]*self.scale, self.__selected[1]*self.scale, self.scale, self.scale)
    @property
    def Selected(self): return self.__selected
    def move_left(self):
        if 0 < self.Selected[0]: self.Selected[0] = self.Selected[0] - 1; GraphicView.viewport().update();
    def move_right(self):
        if self.Selected[0] < GraphicView.Scene.Drawable.Pixmap.width()-1: self.Selected[0] = self.Selected[0] + 1; GraphicView.viewport().update();
    def move_up(self):
        if 0 < self.Selected[1]: self.Selected[1] = self.Selected[1] - 1; GraphicView.viewport().update();
    def move_down(self):
        if self.Selected[1] < GraphicView.Scene.Drawable.Pixmap.height()-1: self.Selected[1] = self.Selected[1] + 1; GraphicView.viewport().update();
    def drawPixel(self):
        painter = QtGui.QPainter(GraphicView.Scene.Drawable.Pixmap)
        painter.setBrush(self.__draw_color)
        painter.setPen(self.__draw_color)
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_Source)
        painter.drawLine(self.Selected[0], self.Selected[1], self.Selected[0], self.Selected[1])
        painter.end()
        self.__update_frame_list()
    def erasePixel(self):
        painter = QtGui.QPainter(GraphicView.Scene.Drawable.Pixmap)
        painter.setBrush(QtCore.Qt.transparent)
        painter.setPen(QtCore.Qt.transparent)
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_Source)
        painter.drawLine(self.Selected[0], self.Selected[1], self.Selected[0], self.Selected[1])
        painter.end()
        self.__update_frame_list()
    def draw_move_left(self):
        if 0 < self.Selected[0]: self.drawPixel(); self.Selected[0] = self.Selected[0] - 1; self.drawPixel(); GraphicView.viewport().update();
    def draw_move_right(self):
        if self.Selected[0] < GraphicView.Scene.Drawable.Pixmap.width()-1: self.drawPixel(); self.Selected[0] = self.Selected[0] + 1; self.drawPixel(); GraphicView.viewport().update();
    def draw_move_up(self):
        if 0 < self.Selected[1]: self.drawPixel(); self.Selected[1] = self.Selected[1] - 1; self.drawPixel(); GraphicView.viewport().update();
    def draw_move_down(self):
        if self.Selected[1] < GraphicView.Scene.Drawable.Pixmap.height()-1: self.drawPixel(); self.Selected[1] = self.Selected[1] + 1; self.drawPixel(); GraphicView.viewport().update();
    def erase_move_left(self):
        if 0 < self.Selected[0]: self.erasePixel(); self.Selected[0] = self.Selected[0] - 1; self.erasePixel(); GraphicView.viewport().update();
    def erase_move_right(self):
        if self.Selected[0] < GraphicView.Scene.Drawable.Pixmap.width()-1: self.erasePixel(); self.Selected[0] = self.Selected[0] + 1; self.erasePixel(); GraphicView.viewport().update();
    def erase_move_up(self):
        if 0 < self.Selected[1]: self.erasePixel(); self.Selected[1] = self.Selected[1] - 1; self.erasePixel(); GraphicView.viewport().update();
    def erase_move_down(self):
        if self.Selected[1] < GraphicView.Scene.Drawable.Pixmap.height()-1: self.erasePixel(); self.Selected[1] = self.Selected[1] + 1; self.erasePixel(); GraphicView.viewport().update();
    def __update_frame_list(self):
        for idx in FrameListView.selectedIndexes():
            FrameListView.Model.update_pixmap(idx, GraphicView.Scene.Drawable.Pixmap)
        GraphicView.viewport().update()
        FrameListView.viewport().update()

class DrawToolbox(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.__get_base_url()
        self.layout = QtWidgets.QHBoxLayout()
        self.__create_buttons()
        self.setLayout(self.layout)
    def __get_base_url(self):
        self.base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        self.base_path = os.path.join(self.base_path, 'res', 'icons', 'draw_tools')
    def __get_icon_path(self, name): return os.path.join(self.base_path, name)
    def __set_icon(self, name):
        base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        base_path = os.path.join(base_path, 'res', 'icons', 'draw_tools')
        cursor = QtGui.QCursor(QPixmap(os.path.join(base_path, name)))
        QApplication.setOverrideCursor(cursor)
    def __create_buttons(self):
#        names = ['Pen', 'Line', 'Bucket']
#        names = ['SelectRectangleTool', 'Pen', 'Line']
#        names = ['Pen', 'Line', 'Rectangle', 'Ellipse']
        names = ['Pen', 'Line', 'Bucket', 'Rectangle', 'Ellipse']
        methods = {
            'Pen': lambda: GraphicView.Scene.Drawable.selectedDrawTool('Pen'),
            'Line': lambda: GraphicView.Scene.Drawable.selectedDrawTool('Line'),
            'Bucket': lambda: GraphicView.Scene.Drawable.selectedDrawTool('Bucket'),
            'Rectangle': lambda: GraphicView.Scene.Drawable.selectedDrawTool('Rectangle'),
            'Ellipse': lambda: GraphicView.Scene.Drawable.selectedDrawTool('Ellipse')
        }
        buttons = {}
        for name in names:
            buttons[name] = QtWidgets.QPushButton()
            buttons[name].setIcon(QtGui.QPixmap(self.__get_icon_path(name.lower())))
            buttons[name].clicked.connect(methods[name])
#            GraphicView.Scene.Drawable.selectedDrawTool('Pen')
#            button.setFixedSize(32,32)
            self.layout.addWidget(buttons[name])

class Pixels:
    def __init__(self):
        self.width = 16
        self.height = 16
        self.pixels = numpy.zeros(self.width*self.height, dtype=int).reshape(self.height, self.width)
    @property
    def Pixels(self): return self.pixels
    @property
    def Width(self): return self.width
    @property
    def Height(self): return self.height
    def save(self):
        print(os.getcwd())
        self.save_txt()
        for ext in ('gif', 'png', 'webp'):
            self.save_raster(ext)
        for ext in ('gif', 'png', 'webp'):
            self.save_animation(ext)
    def load(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()[1:]
        if '' == ext: raise Exception('拡張子が必要です。png,gif,webp,txt形式のいずれかに対応しています。')
        elif 'txt' == ext: self.load_txt(file_path)
        elif 'gif' == ext: self.load_gif(file_path)
        elif 'png' == ext: self.load_png(file_path)
        elif 'webp' == ext: self.load_webp(file_path)
        else: raise Exception('拡張子が未対応です。png,gif,webp,txt形式のいずれかに対応しています。')
    def save_txt(self):
        with open(os.path.join(os.getcwd(), 'pixels.txt'), 'w') as f:
            idx = FrameListView.selectedIndexes()
            image = FrameListView.Model.Frames[idx[0].row()].pixmap.toImage()
            pixels = [0 if 0 == image.pixel(x, y) else 1 for y in range(image.height()) for x in range(image.width())]
            pixels = numpy.array(pixels).reshape(image.height(), image.width())
            f.write('\n'.join([''.join(map(str, pixels[y].tolist())) for y in range(image.height())]))
    def load_txt(self, file_path):
        with open(file_path, 'r') as f:
            lines = f.read().split('\n')
            self.height = len(lines)
            self.width = len(lines[0])
            self.pixels = numpy.zeros(self.width*self.height, dtype=int).reshape(self.height, self.width)
            x = 0; y = 0;
            for line in lines:
                for c in line:
                    self.pixels[y][x] = int(c, 16)
                    x += 1
                y += 1
                x = 0

        idx = FrameListView.selectedIndexes()
        image = Image.new('P', (self.width, self.height))
        pixels = numpy.array(self.pixels).reshape(image.width * image.height)
        image.putdata(pixels.tolist())
        image.putpalette([0,0,0,255,255,255])
        image.putalpha(image.convert('1'))
        palette = image.getpalette()
        palette[3] = 255
        palette[4] = 0
        palette[5] = 0
        image.putpalette(palette)
        FrameListView.Model.appendRow(QtGui.QPixmap.fromImage(ImageQt.ImageQt(image.convert('RGBA'))))
    def save_raster(self, ext):
        for index in FrameListView.selectedIndexes():
            qimg = FrameListView.Model.Frames[index.row()].pixmap.toImage()
            if 'webp' == ext:
                image = Image.new('PA', (self.width, self.height))
                image.putdata([qimg.pixel(x,y) for y in range(qimg.width()) for x in range(qimg.height())])
                print(image.getpalette())
                palette = image.getpalette()
                palette[0] = 255
                palette[1] = 0
                palette[2] = 0
                palette = palette[:3]
                image.putpalette(palette)
            else:
                image = Image.new('P', (self.width, self.height))
                image.putdata([0 if 0 == qimg.pixel(x,y) else 1 for y in range(qimg.width()) for x in range(qimg.height())])
                palette = image.getpalette()
                palette[3] = 255
                palette[4] = 0
                palette[5] = 0
                palette = palette[:6]
                image.putpalette(palette)
            print(ext)
            p = {}
            p['optimize'] = True
            p['lossless'] = True
            p['transparency'] = 0
            if 'gif' == ext: p['disposal'] = 2
            if 'webp' == ext: p['background'] = (0,0,0,0)
            image.save(os.path.join(os.getcwd(), 'pixels.' + ext), **p)
    def save_animation(self, ext):
        print(ext)
        if len(FrameListView.Model.Frames) < 2: return
        images = []
        print('save', len(FrameListView.Model.Frames))
        for frame in FrameListView.Model.Frames:
            mode = 'PA' if 'webp' == ext else 'P'
            image = Image.new(mode, (frame.Pixels.Width, frame.Pixels.Height))
            qimg = frame.pixmap.toImage()
            if 'webp' == ext:
                image.putdata([qimg.pixel(x,y) for y in range(qimg.width()) for x in range(qimg.height())])
            else:
                image.putdata([0 if 0 == qimg.pixel(x,y) else 1 for y in range(frame.pixmap.width()) for x in range(frame.pixmap.height())])
            if 'webp' == ext:
                palette = image.getpalette()
                palette[0] = 255
                palette[1] = 0
                palette[2] = 0
                palette = palette[:3]
                image.putpalette(palette)
            else:
                palette = image.getpalette()
                palette[3] = 255
                palette[4] = 0
                palette[5] = 0
                palette = palette[:6]
                image.putpalette(palette)
            images.append(image)
        p = {}
        p['save_all'] = True
        p['append_images'] = images
        p['duration'] = AnimationDurationSetDialog.Duration
        p['loop'] = AnimationDurationSetDialog.Loop
        p['optimize'] = False
        p['transparency'] = 0
        if 'gif' == ext: p['disposal'] = 2
        if 'webp' == ext: p['background'] = (0,0,0,0)
        image.save(os.path.join(os.getcwd(), 'animation.' + ext), **p)
    def load_png(self, file_path):
        image = Image.open(file_path, mode='r')
        frames = [frame.copy() for frame in ImageSequence.Iterator(image)]
        if 1 < len(frames): frames = frames[1:] # なぜか0番目に最後のフレームが入っているため飛ばす
        for frame in frames:
            img = frame.convert('RGBA') # ValueError: unsupported image mode PA 
            FrameListView.Model.appendRow(QtGui.QPixmap.fromImage(ImageQt.ImageQt(img)))
    def load_gif(self, file_path): # 値が0/255で出力されてしまうので0/1に変換する
        with Image.open(file_path, mode='r') as image:
            frames = [frame.copy() for frame in ImageSequence.Iterator(image)]
            if 1 < len(frames): frames = frames[1:] # なぜか0番目に最後のフレームが入っているため飛ばす
            for frame in frames:
                img = frame.convert('RGBA') # ValueError: unsupported image mode PA 
                FrameListView.Model.appendRow(QtGui.QPixmap.fromImage(ImageQt.ImageQt(img)))
    def load_webp(self, file_path): # 値が[0,0,0]/[255,255,255]で出力されてしまうので0/1に変換する
        with Image.open(file_path, mode='r') as image:
            frames = [frame.copy() for frame in ImageSequence.Iterator(image)]
            if 1 < len(frames): frames = frames[1:] # なぜか0番目に最後のフレームが入っているため飛ばす
            for frame in frames:
                print(True if 'default_image' in frame.info else False)
                img = frame.convert('RGBA') # ValueError: unsupported image mode PA 
                FrameListView.Model.appendRow(QtGui.QPixmap.fromImage(ImageQt.ImageQt(img)))
 
class AnimationWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.frame_list = FrameListView()
        globals()['FrameListView'] = self.frame_list
        self.label = AnimationLabel()
        globals()['AnimationLabel'] = self.label
        layout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.LeftToRight)
        layout.addWidget(self.label)
        layout.addWidget(self.frame_list)
        self.setLayout(layout)
    @property
    def Label(self): return self.label
    @property
    def FrameListView(self): return self.frame_list

class AnimationLabel(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.__is_stop = True
        self.__frame_index = 0
        self.start_animation()
    def mousePressEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton:
            self.toggle_animation()
    def start_animation(self):
        self.setPixmap(FrameListView.Model.Frames[self.__frame_index].Icon.pixmap(16,16))
        if not self.__is_stop:
            if self.__frame_index < FrameListView.Model.rowCount()-1: self.__frame_index += 1
            else: self.__frame_index = 0
            QtCore.QTimer.singleShot(AnimationDurationSetDialog.Duration, self.start_animation)
    def toggle_animation(self):
        self.__is_stop = not self.__is_stop
        self.start_animation()
        
class FrameListView(QtWidgets.QListView):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.resizeContents(16*16, 16)
        self.model = FrameListModel()
        self.model.appendRow()
        self.setModel(self.model)
        globals()['FrameListModel'] = self.model

#        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
#        self.setDragEnabled(True)
#        self.viewport().setAcceptDrops(True)
#        self.setAcceptDrops(True)
#        self.setDropIndicatorShown(True)
#        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)

        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.setDefaultDropAction(QtCore.Qt.MoveAction)


        self.resize(16*32, 32)
        self.setCurrentIndex(self.model.index(0,0))
        self.setFlow(QtWidgets.QListView.LeftToRight)
        self.duration_dialog = AnimationDurationSetDialog()
        globals()['AnimationDurationSetDialog'] = self.duration_dialog
        self.show()
    def mouseMoveEvent(self, event):
        super(self.__class__, self).mousePressEvent(event)
    def mousePressEvent(self, event):
        super(self.__class__, self).mousePressEvent(event)
        for idx in self.selectedIndexes():
            frame = idx.data(QtCore.Qt.UserRole)
            Drawable.Pixels = frame.Pixels
            Drawable.pixmap = frame.pixmap
            Window.widget.view.scene().update()
        if event.buttons() & QtCore.Qt.RightButton:
            self.duration_dialog.show()
    def update_pixmap(self, pixmap):
        for idx in self.selectedIndexes():
            self.model.update_pixmap(idx, pixmap)
    @property
    def Model(self): return self.model
    def __add_frame(self):
        self.model.appendRow()
        self.setCurrentIndex(self.model.index(len(self.model.Frames)-1,0))
        self.__show_drawable()
    def __insert_new_frame(self):
        idx = self.selectedIndexes()
        self.model.insertRow(idx.row())
        self.__show_drawable()
    def __insert_copy_frame(self):
        idx = self.selectedIndexes()
        self.model.insertRow(idx[0].row(), self.model.Frames[idx[0].row()].pixmap.copy())
        self.__show_drawable()
    def __delete_frame(self):
        if len(self.model.Frames) < 2: return
        for idx in self.selectedIndexes():
            if idx.row() == self.model.rowCount()-1:
                self.setCurrentIndex(self.model.index(idx.row()-1,0))
            else:
                self.setCurrentIndex(self.model.index(idx.row(),0))
            self.model.removeRow(idx)
        self.__show_drawable()
    def __show_drawable(self):
        for idx in self.selectedIndexes():
            frame = idx.data(QtCore.Qt.UserRole)
            Drawable.pixmap = frame.pixmap.copy()
            Window.widget.view.scene().update()
    def __selected_previous_frame(self):
        idx = self.selectedIndexes()
        if 0 < idx[0].row():
            self.setCurrentIndex(self.model.index(idx[0].row()-1,0))
        self.__show_drawable()
    def __selected_next_frame(self):
        idx = self.selectedIndexes()
        if idx[0].row() < self.model.rowCount()-1:
            self.setCurrentIndex(self.model.index(idx[0].row()+1,0))
        self.__show_drawable()
    def __move_previous_frame(self):
        idx = self.selectedIndexes()
        if 0 < idx[0].row():
            self.model.movePreviousRow(idx[0].row())
        self.__show_drawable()
    def __move_next_frame(self):
        idx = self.selectedIndexes()
        if idx[0].row() < self.model.rowCount()-1:
            self.model.moveNextRow(idx[0].row())
        self.__show_drawable()
        
class ActionCreator:
    Actions = {}
    @classmethod
    def create(self, name, text, triggered, shortcut):
#        print(name, text, triggered, shortcut)
        if name in ActionCreator.Actions.keys(): raise Exception("ERROR: Actionのname'{}'が重複しています。別のnameにしてください。".format(name))
        a = QtWidgets.QAction()
        if name: a.setObjectName(name)
        else: raise Exception("ERROR: Actionのnameを設定してください。")
        if text: a.setText(text)
        if shortcut: a.setShortcut(shortcut)
        if triggered:
            methods = triggered.split('.')
#            print(methods)
            if len(methods) < 2: raise Exception("ERROR: Actionのmethodはeval()で参照できる名前にしてください。'.'で分割します。1個目はglobals()内にあるインスタンス。最後はメソッド。")
            else:
#                print(FrameListView._FrameListView__add_frame)
                m = eval(triggered)
                a.triggered.connect(m)
        ActionCreator.Actions[name] = a
        return ActionCreator.Actions[name]

#class FrameListModel(QtGui.QStandardItemModel):
class FrameListModel(QtCore.QAbstractListModel):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.frames = []
    def rowCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid(): return 0
        return len(self.frames)
    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DecorationRole:
            return self.frames[index.row()].Icon
        elif  role == QtCore.Qt.UserRole:
            return self.frames[index.row()]
    def appendRow(self, pixmap=None):
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        self.frames.append(Frame(pixmap))
        self.endInsertRows()
    def insertRow(self, index, pixmap=None):
        self.beginInsertRows(QtCore.QModelIndex(), index, index)
        self.frames.insert(index, Frame(pixmap))
        self.endInsertRows()
    def removeRow(self, index):
        self.beginRemoveRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        print(index.row())
        self.frames.pop(index.row())
        self.endRemoveRows()
    def movePreviousRow(self, index):
        self.beginMoveRows(QtCore.QModelIndex(), index, index, QtCore.QModelIndex(), index-1)
        self.frames.insert(index-1, self.frames.pop(index))
        self.endMoveRows()
    def moveNextRow(self, index):
        self.beginMoveRows(QtCore.QModelIndex(), index, index, QtCore.QModelIndex(), index+2)
        self.frames.insert(index+1, self.frames.pop(index))
        self.endMoveRows()
    def update_pixmap(self, index, pixmap):
        self.frames[index.row()].update_pixmap(pixmap)
    @property
    def Frames(self): return self.frames
    def supportedDropActions(self):
        return QtCore.Qt.CopyAction | QtCore.Qt.MoveAction
    def flags(self, index): # http://www.walletfox.com/course/qtreorderablelist.php
        defaultFlags = super(self.__class__, self).flags(index)
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled  | defaultFlags


class Frame:
    def __init__(self, pixmap=None):
        self.pixels = Pixels()
        if pixmap: self.pixmap = pixmap
        else:
            img = QtGui.QImage(self.pixels.Width, self.pixels.Height, QtGui.QImage.Format_ARGB32)
            img.fill(QtGui.QColor(0,0,0,0))
            self.pixmap = QtGui.QPixmap.fromImage(img)
        self.icon = QtGui.QImage(self.pixels.Width, self.pixels.Height, QtGui.QImage.Format_Mono)
        self.update_pixmap(self.pixmap)
    def __init_pixmap(self):
        painter = QtGui.QPainter(self.pixmap)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(0,0,0), QtCore.Qt.SolidPattern))
        painter.fillRect(self.pixmap.rect(), QtGui.QColor(0,0,0))
        painter.end()
    def update_pixmap(self, pixmap):
        self.pixmap = pixmap
        self.icon = QtGui.QIcon(pixmap)
    @property
    def Pixels(self): return self.pixels
    @Pixels.setter
    def Pixels(self, value): self.pixels = value
    @property
    def Icon(self): return self.icon
    @Icon.setter
    def Icon(self, value): self.icon = value

class AnimationDurationSetDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setWindowTitle("Set duration")
        self.duration = QtWidgets.QSpinBox()
        self.loop = QtWidgets.QSpinBox()
        self.duration.setMinimum(0)
        self.duration.setMaximum(1000*60*60*24)
        self.duration.setSingleStep(1)
        self.loop.setMinimum(0)
        self.loop.setMaximum(2**30)
        self.loop.setSingleStep(1)
        self.duration.setValue(100)
        self.loop.setValue(0)
        layout = QtWidgets.QFormLayout()
        layout.addRow("Duration", self.duration)
        layout.addRow("Loop time", self.loop)
        self.setLayout(layout)
        self.x = self.geometry().x()
        self.y = self.geometry().y()
        self.w = 0
        self.h = 0
    def show(self):
        self.setGeometry(self.x, self.y, self.w, self.h)
        super(self.__class__, self).show()
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.x = self.geometry().x()
            self.y = self.geometry().y()
            self.w = self.geometry().width()
            self.h = self.geometry().height()
        super(self.__class__, self).keyPressEvent(event)
    @property
    def Duration(self): return self.duration.value()
    @property
    def Loop(self): return self.loop.value()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())

