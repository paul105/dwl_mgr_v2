#-*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore

####okno pobierania
class UI_dl(QtGui.QMainWindow):
    def __init__(self,n):
        QtGui.QMainWindow.__init__(self)
        self.cw3 = QtGui.QWidget(self)
        self.setCentralWidget(self.cw3)
        self.setWindowTitle("Pobieranie pliku...")
        self.end = QtGui.QPushButton("Zakoncz", self.cw3)
        self.end.setGeometry(QtCore.QRect(250,250,100,30))
        self.end.setEnabled(False)
        self.connect(self.end, QtCore.SIGNAL("clicked()"), self.close)
        self.tableParts = QtGui.QTableWidget(self.cw3)
        self.tableParts.setGeometry(QtCore.QRect(10, 10, 300, 200))
        self.tableParts.horizontalHeader().setVisible(False)
        self.tableParts.horizontalHeader().setStretchLastSection(True)
        self.tableParts.setObjectName("tableParts")
        self.tableParts.setColumnCount(1)



def setTableParts(table,n):
    table.setRowCount(n)
    for i in range(0,n):
        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
        table.setItem(i, 0, item)

