#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, os, numpy, PIL, csv
from PySide2 import QtCore, QtGui, QtWidgets
from PIL import Image, ImagePalette, ImageQt, ImageSequence

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setAcceptDrops(True)
        self.setWindowTitle("pixpeer")
        self.widget = FrameListView()
        self.setCentralWidget(self.widget)
        globals()['Window'] = self
        self.show()

class FrameListView(QtWidgets.QListView):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.resizeContents(16*16, 16)
#        self.model = FrameListModel()
        self.model = MyStandardItemModel()
        """
        self.model = QtGui.QStandardItemModel()
        self.model.appendRow(QtGui.QStandardItem('A'))
        self.model.appendRow(QtGui.QStandardItem('B'))
        self.model.appendRow(QtGui.QStandardItem('C'))
        """
        self.setModel(self.model)
        globals()['FrameListModel'] = self.model

        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.setDragEnabled(True)
#        self.viewport().setAcceptDrops(True)
        self.setAcceptDrops(True)
#        self.setDropIndicatorShown(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
#        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.setDefaultDropAction(QtCore.Qt.MoveAction)
    def supportedDropActions(self):
#        return QtCore.Qt.MoveAction
        return QtCore.Qt.CopyAction | QtCore.Qt.MoveAction

class MyStandardItemModel(QtGui.QStandardItemModel):
    def __init__(self):
        super(self.__class__, self).__init__()
        for label in ['A', 'B', 'C']:
            item = QtGui.QStandardItem(label)
            item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled)
            self.appendRow(item)

#class FrameListModel(QtCore.QAbstractItemModel):
class FrameListModel(QtCore.QAbstractListModel):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.__datas = []
        d1 = {}; d1[QtCore.Qt.DisplayRole] = 'A';
        d2 = {}; d2[QtCore.Qt.DisplayRole] = 'B';
        d3 = {}; d3[QtCore.Qt.DisplayRole] = 'C';
        d4 = {}; d4[QtCore.Qt.DisplayRole] = 'D';
        self.__datas.append(d1)
        self.__datas.append(d2)
        self.__datas.append(d3)
        self.__datas.append(d4)

    def rowCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid(): return 0
        return len(self.__datas)
#        return len(self.frames)
    def data(self, index, role=QtCore.Qt.DisplayRole):# https://doc.qt.io/qtforpython/PySide2/QtCore/Qt.html
        if role == QtCore.Qt.DisplayRole:
            return self.__datas[index.row()][role]
#        if role == QtCore.Qt.DecorationRole:
#            return self.frames[index.row()].Icon
#        elif  role == QtCore.Qt.UserRole:
#            return self.frames[index.row()]
    def appendRow(self, value=None):
#    def appendRow(self, pixmap=None):
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        d1 = {}; d1[QtCore.Qt.DisplayRole] = value if value else 'C';
        self.__datas.append(d1)
#        self.frames.append(Frame(pixmap))
        self.endInsertRows()
    def flag(self, index): # http://www.walletfox.com/course/qtreorderablelist.php
        defaultFlags = super(self.__class__, self).flag(index)
#        if index.isValid(): return QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled | defaultFlags;
#        if index.isValid(): return QtCore.Qt.ItemIsDragEnabled | defaultFlags;
#        else: return QtCore.Qt.ItemIsDropEnabled | defaultFlags
        if index.isValid(): return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled
        else: return defaultFlags

class MyStandardItemModel2(QtGui.QStandardItemModel):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.__datas = []
        for label in ['A', 'B', 'C']:
            item = QtGui.QStandardItem(label)
            item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled)
#            self.appendRow(item)
            self.appendRow(label)
    def rowCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid(): return 0
        return len(self.__datas)
    def data(self, index, role=QtCore.Qt.DisplayRole):# https://doc.qt.io/qtforpython/PySide2/QtCore/Qt.html
        if role == QtCore.Qt.DisplayRole:
            return self.__datas[index.row()][role]
    def appendRow(self, value=None):
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        d1 = {}; d1[QtCore.Qt.DisplayRole] = value if value else 'C';
        self.__datas.append(d1)
#        self.__datas.append(value)
        self.endInsertRows()
    def flag(self, index): # http://www.walletfox.com/course/qtreorderablelist.php
        defaultFlags = super(self.__class__, self).flag(index)
#        if index.isValid(): return QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled | defaultFlags;
#        if index.isValid(): return QtCore.Qt.ItemIsDragEnabled | defaultFlags;
#        else: return QtCore.Qt.ItemIsDropEnabled | defaultFlags
        if index.isValid(): return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled
        else: return defaultFlags
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())

