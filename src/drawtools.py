#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, os, numpy, PIL, csv
from PySide2 import QtCore, QtGui, QtWidgets
from PIL import Image, ImagePalette, ImageQt, ImageSequence
from abc import ABCMeta, abstractmethod
from skimage.segmentation import flood_fill

class DrawTool:
    def __init__(self, *args, **kwargs):
        self.points = []
        self.color = QtGui.QColor(255,0,0)
        self.editing_color = QtGui.QColor(255,0,0,96)
    @property
    def Points(self): return self.points
    @property
    def Color(self): return self.color
    @property
    def EditingColor(self): return self.editing_color
    @Color.setter
    def Color(self, value):
        if isinstance(value, QtGui.QColor): self.color = value
    @EditingColor.setter
    def EditingColor(self, value):
        if isinstance(value, QtGui.QColor): self.editing_color = value
    def begin(self, x, y, pixmap):
        self.points.clear()
        self.editing(x, y, pixmap)
    def editing(self, x, y, pixmap):
        self.points.append([x, y])
    def end(self, x, y, pixmap):
        self.points.append([x, y])

class SelectRectangleTool(DrawTool):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.Points.append([0,0])
        self.Points.append([0,0])
        self.pen = QtGui.QPen()
        self.pen.setStyle(QtCore.Qt.DashDotLine)
        self.pen.setWidth(3)
        self.pen.setColor(QtGui.QColor(0,255,0))
    def begin(self, x, y, pixmap):
        self.Points[0][0], self.Points[0][1] = x, y
        self.Points[1][0], self.Points[1][1] = x, y
    def __setEndPos(self, x, y):
        self.points[1][0], self.points[1][1] = x, y
    def editing(self, x, y, pixmap):
        self.__setEndPos(x, y)
        self.__draw(pixmap, self.EditingColor)
    def end(self, x, y, pixmap):
        self.__setEndPos(x, y)
        self.__draw(pixmap, self.Color)
    def __draw(self, pixmap, color):
        painter = QtGui.QPainter(pixmap)
        painter.setBrush(color)
#        painter.setPen(color)
        painter.setPen(self.pen)
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_Source)
        if 1 == len(self.points):
            painter.drawLine(self.points[0][0], self.points[0][1], self.points[0][0], self.points[0][1])
        elif 1 < len(self.points):
            for i in range(len(self.points)-1):
                painter.drawRect(self.points[i][0], self.points[i][1], self.points[i+1][0], self.points[i+1][1])
        painter.end()

class BucketTool(DrawTool):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.__selected_color = None
        self.__pixels = []
    def begin(self, x, y, pixmap):
        self.Points.clear()
        self.Points.append([x, y])
        self.__selected_color = pixmap.toImage().pixelColor(x, y)
        self.__draw(pixmap, self.EditingColor)
    def editing(self, x, y, pixmap):
        self.Points[0][0], self.Points[0][1] = x, y
        self.__draw(pixmap, self.EditingColor)
    def end(self, x, y, pixmap):
        self.Points[0][0], self.Points[0][1] = x, y
        self.__draw(pixmap, self.Color)
    def __draw(self, pixmap, color):
        img = pixmap.toImage()
        pixels = [0 if 0 == img.pixel(x, y) else 1 for y in range(img.height()) for x in range(img.width())]
        pixels = numpy.array(pixels).reshape(img.height(), img.width())
#        print(pixels)
        pixels = flood_fill(pixels, (self.Points[0][0], self.Points[0][1]), 1, connectivity=1)
#        print(pixels)
        painter = QtGui.QPainter(pixmap)
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_Source)
        painter.fillRect(img.rect(), QtCore.Qt.transparent)
        painter.drawImage(0, 0, QtGui.QImage(pixels, img.width(), img.height(), QtGui.QImage.Format_ARGB32))
        for y in range(pixmap.height()):
            for x in range(pixmap.width()):
                painter.setPen(QtGui.QColor.fromRgba(0 if 0 == pixels[y][x] else self.Color.rgba()))
                painter.drawPoint(x, y)
        painter.end()
         
class PenTool(DrawTool):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
    def editing(self, x, y, pixmap):
        super(self.__class__, self).editing(x, y, pixmap)
        self.__draw(pixmap, self.EditingColor)
    def end(self, x, y, pixmap):
        super(self.__class__, self).end(x, y, pixmap)
        self.__draw(pixmap, self.Color)
        self.points.clear()
    def __draw(self, pixmap, color):
        painter = QtGui.QPainter(pixmap)
        painter.setBrush(color)
        painter.setPen(color)
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_Source)
        if 1 == len(self.points):
            painter.drawLine(self.points[0][0], self.points[0][1], self.points[0][0], self.points[0][1])
        elif 1 < len(self.points):
            for i in range(len(self.points)-1):
                painter.drawLine(self.points[i][0], self.points[i][1], self.points[i+1][0], self.points[i+1][1])
        painter.end()

class LineTool(DrawTool):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.Points.append([0,0])
        self.Points.append([0,0])
    def begin(self, x, y, pixmap):
        self.Points[0][0], self.Points[0][1] = x, y
        self.Points[1][0], self.Points[1][1] = x, y
    def __setEndPos(self, x, y):
        self.points[1][0], self.points[1][1] = x, y
    def editing(self, x, y, pixmap):
        self.__setEndPos(x, y)
        self.__draw(pixmap, self.EditingColor)
    def end(self, x, y, pixmap):
        self.__setEndPos(x, y)
        self.__draw(pixmap, self.Color)
    def __draw(self, pixmap, color):
        painter = QtGui.QPainter(pixmap)
        painter.setBrush(color)
        painter.setPen(color)
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_Source)
        if 1 == len(self.points):
            painter.drawLine(self.points[0][0], self.points[0][1], self.points[0][0], self.points[0][1])
        elif 1 < len(self.points):
            for i in range(len(self.points)-1):
                painter.drawLine(self.points[i][0], self.points[i][1], self.points[i+1][0], self.points[i+1][1])
        painter.end()

class RectangleTool(DrawTool):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.Points.append([0,0])
        self.Points.append([0,0])
        self.pen = QtGui.QPen()
        self.pen.setStyle(QtCore.Qt.SolidLine)
        self.pen.setWidth(1)
#        self.pen.setColor(QtGui.QColor(255,0,0))
    def begin(self, x, y, pixmap):
        self.Points[0][0], self.Points[0][1] = x, y
        self.Points[1][0], self.Points[1][1] = x, y
    def __setEndPos(self, x, y):
        self.points[1][0], self.points[1][1] = x, y
    def editing(self, x, y, pixmap):
        self.__setEndPos(x, y)
        self.__draw(pixmap, self.EditingColor)
    def end(self, x, y, pixmap):
        self.__setEndPos(x, y)
        self.__draw(pixmap, self.Color)
    def __draw(self, pixmap, color):
        painter = QtGui.QPainter(pixmap)
#        painter.setBrush(color)
#        painter.setPen(color)
        self.pen.setColor(color)
        painter.setPen(self.pen)
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_Source)
        if 1 == len(self.points):
            painter.drawLine(self.points[0][0], self.points[0][1], self.points[0][0], self.points[0][1])
        elif 1 < len(self.points):
            painter.drawRect(self.points[0][0], self.points[0][1], self.points[1][0], self.points[1][1])
        painter.end()

class EllipseTool(DrawTool):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.Points.append([0,0])
        self.Points.append([0,0])
        self.pen = QtGui.QPen()
        self.pen.setStyle(QtCore.Qt.SolidLine)
        self.pen.setWidth(1)
#        self.pen.setColor(QtGui.QColor(255,0,0))
    def begin(self, x, y, pixmap):
        self.Points[0][0], self.Points[0][1] = x, y
        self.Points[1][0], self.Points[1][1] = x, y
    def __setEndPos(self, x, y):
        self.points[1][0], self.points[1][1] = x, y
    def editing(self, x, y, pixmap):
        self.__setEndPos(x, y)
        self.__draw(pixmap, self.EditingColor)
    def end(self, x, y, pixmap):
        self.__setEndPos(x, y)
        self.__draw(pixmap, self.Color)
    def __draw(self, pixmap, color):
        painter = QtGui.QPainter(pixmap)
#        painter.setBrush(color)
#        painter.setPen(color)
        self.pen.setColor(color)
        painter.setPen(self.pen)
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_Source)
        if 1 == len(self.points):
            painter.drawLine(self.points[0][0], self.points[0][1], self.points[0][0], self.points[0][1])
        elif 1 < len(self.points):
            painter.drawEllipse(self.points[0][0], self.points[0][1], self.points[1][0], self.points[1][1])
        painter.end()

