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
        self.model = MyStandardItemModel()
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

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())

