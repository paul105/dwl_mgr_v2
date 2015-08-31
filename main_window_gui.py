#-*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from download_choice_gui import Download_choice_window_gui
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


def set_file_download_list(file_download_list):
    try:
        with open("files","rb") as download_list_file:
            _lines_in_list = download_list_file.readlines()
            file_download_list.setRowCount(len(_lines_in_list))
            for line in _lines_in_list:
                file_informations = json.loads(line)
                name = QtGui.QTableWidgetItem(file_informations["name"])
                name.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
                date = QtGui.QTableWidgetItem(file_informations["date"])
                date.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
                url1 = str(file_informations["url1"])
                try:
                    url2 = '{}'.format(file_informations["url2"])
                except:
                    url2 = ''
                finally:
                    url2 = QtGui.QTableWidgetItem(url2)
                    url2.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
                url = QtGui.QTableWidgetItem(url1)
                url.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
                file_download_list.setItem(_lines_in_list.index(line), 0, name)
                file_download_list.setItem(_lines_in_list.index(line), 1, date)
                file_download_list.setItem(_lines_in_list.index(line), 2, url)
                file_download_list.setItem(_lines_in_list.index(line), 3, url2)
                file_download_list.resizeColumnsToContents()
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
        self.file_download_list.setColumnCount(4)
        self.file_download_list.setRowCount(0)
        set_file_download_list(self.file_download_list)

        # result = QtGui.QMessageBox
        # result.question(self, 'Usun plik', 'Czy chcesz usunac plik rowniez z dysku?', QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | QtGui.QMessageBox.Cancel, QtGui.QMessageBox.No)


        ###signals and slots

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

            self.set_file_download_list()
        except:
            pass

    def set_file_download_list(self):
        try:
            with open("files","rb") as download_list_file:
                _lines_in_list = download_list_file.readlines()
                self.file_download_list.setRowCount(len(_lines_in_list))
                for line in _lines_in_list:
                    file_informations = json.loads(line)
                    name = QtGui.QTableWidgetItem(file_informations["name"])
                    name.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
                    date = QtGui.QTableWidgetItem(file_informations["date"])
                    date.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
                    url1 = str(file_informations["url1"])
                    try:
                        url2 = '{}'.format(file_informations["url2"])
                    except:
                        url2 = ''
                    finally:
                        url2 = QtGui.QTableWidgetItem(url2)
                        url2.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
                    url = QtGui.QTableWidgetItem(url1)
                    url.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
                    self.file_download_list.setItem(_lines_in_list.index(line), 0, name)
                    self.file_download_list.setItem(_lines_in_list.index(line), 1, date)
                    self.file_download_list.setItem(_lines_in_list.index(line), 2, url)
                    self.file_download_list.setItem(_lines_in_list.index(line), 3, url2)
                    self.file_download_list.resizeColumnsToContents()
        except:
            pass


    def new_download_choice_gui(self):
        self.new_download_choice_gui_handle = Download_choice_window_gui(self.file_download_list)
        self.new_download_choice_gui_handle.setGeometry(QtCore.QRect(100, 100, 600, 400))
        self.new_download_choice_gui_handle.show()
        return self.new_download_choice_gui_handle





