#-*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from download_choice_gui import download_choice_window_gui
import json

###application class
class App(QtGui.QApplication):
    def __init__(self, *args):
        QtGui.QApplication.__init__(self, *args)
        self.main = MainWindow()
        self.main.setGeometry(QtCore.QRect(100,100,800,600))
        self.connect(self, QtCore.SIGNAL("lastWindowClosed()"), self.byebye )
        self.main.show()
    def byebye( self ):
        self.exit(0)


def _set_file_download_list(table):
    try:
        with open("files","rb") as download_list_file:
            _lines_in_list = download_list_file.readlines()
            table.setRowCount(len(_lines_in_list))
            for i in range(0,len(_lines_in_list)):
                file_informations = json.loads(_lines_in_list[i])

                name = QtGui.QTableWidgetItem(file_informations["name"])
                name.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
                date = QtGui.QTableWidgetItem(file_informations["date"])
                date.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
                url = QtGui.QTableWidgetItem(str(file_informations["url"]))
                url.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
                table.setItem(i, 0, name)
                table.setItem(i, 1, date)
                table.setItem(i, 2, url)
    except:
        pass

###main window class
class MainWindow(QtGui.QMainWindow):
    def __init__(self, *args):
        QtGui.QMainWindow.__init__(self, *args)
        self.centralWidget = QtGui.QWidget(self)
        self.setWindowTitle("Pobieracz")
        self.setCentralWidget(self.centralWidget)

        ###buttons and others
        self.new_download = QtGui.QPushButton("Nowy", self.centralWidget)
        self.new_download.setGeometry(QtCore.QRect(10, 10, 100, 60))

        self._delete_from_list = QtGui.QPushButton("Usun", self.centralWidget)
        self._delete_from_list.setGeometry(QtCore.QRect(10, 130, 100, 60))

        self.file_download_list = QtGui.QTableWidget(self.centralWidget)
        self.file_download_list.setGeometry(QtCore.QRect(145, 130, 630, 400))
        self.file_download_list.horizontalHeader().setVisible(False)
        self.file_download_list.horizontalHeader().setStretchLastSection(True)
        self.file_download_list.setObjectName("File download list")
        self.file_download_list.setColumnCount(3)
        self.file_download_list.setRowCount(0)

        ###signals and slots
        _set_file_download_list(self.file_download_list)
        self.connect(self.new_download, QtCore.SIGNAL("clicked()"), self.new_download_choice_gui)
        self.connect(self._delete_from_list, QtCore.SIGNAL("clicked()"), self._delete_row_file_download_list)

    def _delete_row_file_download_list(self):
        list_current_row = self.file_download_list.currentRow()
        try:
            with open("files","rb") as download_list_file:
                _lines_in_list = download_list_file.readlines()
                del _lines_in_list[list_current_row]
                with open("files","wb") as download_list_file2:
                    [download_list_file2.write(_lines_in_list[element]) for element in range(0, len(_lines_in_list))]
            _set_file_download_list(self.file_download_list)
        except:
            pass

    def cos(self):
        pass


    def new_download_choice_gui(self):
        self.new_download_choice_gui_handle = download_choice_window_gui(self.file_download_list)
        self.new_download_choice_gui_handle.setGeometry(QtCore.QRect(100, 100, 600, 400))
        self.new_download_choice_gui_handle.show()
        return self.new_download_choice_gui_handle





