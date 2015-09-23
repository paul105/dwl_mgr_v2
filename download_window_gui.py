#-*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore

####okno pobierania
class UI_dl(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.centralWidget = QtGui.QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.setWindowTitle("Pobieranie pliku...")

        self.finish_button = QtGui.QPushButton("Zakoncz", self.centralWidget)
        self.finish_button.setGeometry(QtCore.QRect(250,250,100,30))
        self.finish_button.setEnabled(False)

        self.table_download_parts_info = QtGui.QTableWidget(self.centralWidget)
        self.table_download_parts_info.setGeometry(QtCore.QRect(10, 10, 300, 200))
        self.table_download_parts_info.horizontalHeader().setVisible(False)
        self.table_download_parts_info.horizontalHeader().setStretchLastSection(True)
        self.table_download_parts_info.setObjectName("tableParts")
        self.table_download_parts_info.setColumnCount(1)

        self.connect(self.finish_button, QtCore.SIGNAL("clicked()"), self.finish_button_click)

    def set_table_download_parts_info_rows(self,row_count):
        self.table_download_parts_info.setRowCount(row_count)
        for row in range(0,row_count):
            item = QtGui.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
            self.table_download_parts_info.setItem(row, 0, item)

    def finish_button_click(self):
        self.close()
