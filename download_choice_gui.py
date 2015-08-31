#-*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
from download_window_gui import UI_dl
import myFile_api
import supervisor_api

###window to input download choice class
class Download_choice_window_gui(QtGui.QMainWindow):
    def __init__(self, file_download_list):
        QtGui.QMainWindow.__init__(self)
        self.file_download_list = file_download_list
        self.dir = ""
        self.centralWidget = QtGui.QWidget(self)
        self.setWindowTitle("Nowe Pobieranie")
        self.setCentralWidget(self.centralWidget)

        #buttons and others
        self.url1 = QtGui.QLineEdit(self.centralWidget)
        self.url1.setGeometry(QtCore.QRect(150,100,400,30))
        self.url1.setObjectName("url_1")

        self.parts = QtGui.QLineEdit(self.centralWidget)
        self.parts.setGeometry(QtCore.QRect(40,100,40,30))
        self.parts.setObjectName("Parts")

        self.urlBox = QtGui.QCheckBox(self.centralWidget)
        self.urlBox.setGeometry(QtCore.QRect(50, 170, 70, 17))
        self.urlBox.setObjectName("urlBox")

        self.url2 = QtGui.QLineEdit(self.centralWidget)
        self.url2.setGeometry(QtCore.QRect(150,160,400,30))
        self.url2.setObjectName("url_2")
        self.url2.setDisabled(True)

        self.proportion_slider = QtGui.QSlider(self.centralWidget)
        self.proportion_slider.setGeometry(QtCore.QRect(150, 220, 400, 30))
        self.proportion_slider.setOrientation(QtCore.Qt.Horizontal)
        self.proportion_slider.setObjectName("Proportion slider")
        self.proportion_slider.setDisabled(True)
        self.proportion_slider.setValue(50)
        self.proportion_slider.setRange(0,100)

        self.proportion_value = QtGui.QLineEdit(self.centralWidget)
        self.proportion_value.setGeometry(QtCore.QRect(40,220,40,30))
        self.proportion_value.setObjectName("Proportion Value")
        self.proportion_value.setDisabled(True)
        self.proportion_value.setText(str(self.proportion_slider.value()))
        self.proportion_value.setMouseTracking(False)
        self.proportion_value.setMaxLength(3)

        self.__search = QtGui.QPushButton("Przegladaj", self.centralWidget)
        self.__search.setGeometry(QtCore.QRect(10,10,100,30))

        self.start_new_downloading = QtGui.QPushButton("Dodaj", self.centralWidget)
        self.start_new_downloading.setGeometry(QtCore.QRect(400,300,150,70))

        ###signals and slots
        self.connect(self.__search, QtCore.SIGNAL("clicked()"), self._set_directory_to_save)
        self.connect(self.start_new_downloading, QtCore.SIGNAL("clicked()"), self.start_new_download)
        self.connect(self.urlBox, QtCore.SIGNAL("clicked()"), self.change_urlBox_check_status)
        self.connect(self.proportion_slider, QtCore.SIGNAL("valueChanged(int)"), self._get_value_from_slider_and_set_value_box)
        self.connect(self.proportion_value, QtCore.SIGNAL("textEdited(QString)"), self._get_value_from_box_and_set_slider)

    def _get_value_from_box_and_set_slider(self):
        x = self.proportion_value.text()
        try:
            x = int(x)
        except:
            x = ""
            self.proportion_value.clear()
        if x == "":
            self.proportion_value.setMaxLength(3)
        if len(str(x)) == 1:
            if x > 1 and x < 10 :
                self.proportion_value.setMaxLength(2)
            elif x == 0:
                self.proportion_value.setMaxLength(1)
            elif x == 1:
                self.proportion_value.setMaxLength(3)
            else:
                self.proportion_value.clear()
                self.proportion_value.setMaxLength(3)
        elif len(str(x)) == 2:
            if x == 10:
                self.proportion_value.setMaxLength(3)
            elif x > 9 and x < 100:
                self.proportion_value.setMaxLength(2)
            else:
                self.proportion_value.clear()
                self.proportion_value.setMaxLength(3)
        elif len(str(x)) == 3:
            if not x == 100:
                self.proportion_value.setText("100")
                x = 100
        if not x == "":
            self.proportion_slider.setValue(x)
        else:
            self.proportion_slider.setValue(0)


    def _get_value_from_slider_and_set_value_box(self):
        self.proportion_value.setText(str(self.proportion_slider.value()))

    def change_urlBox_check_status(self):
        if self.urlBox.isChecked():
            self.url2.setDisabled(False)
            self.proportion_slider.setDisabled(False)
            self.proportion_value.setDisabled(False)
        else:
            self.url2.setDisabled(True)
            self.proportion_slider.setDisabled(True)
            self.proportion_value.setDisabled(True)
        return None

    def get_url1(self):
        url = str(self.url1.text())
        return url

    def get_url2(self):
        url = str(self.url2.text())
        return url

    def get_parts(self):
        try:
            parts = int(self.parts.text())
        except:
            parts = ""
        finally:
            return parts


    def _set_directory_to_save(self):
        fd = QtGui.QFileDialog(self)
        self.dir = str(fd.getExistingDirectory(self))
        from os.path import isdir
        try:
            if not isdir(self.dir):
                self.dir=""
        finally:
            return self.dir

    def _get_directory_to_save(self):
        return self.dir

    def check_url(self,url):
        import urllib2
        try:
            urllib2.urlopen(url)
            return url
        except:
            try:
                url2 = "http://" + (url.split("//",1))[1]
                urllib2.urlopen(url2)
                return url2
            except:
                try:
                    url3 = "http://" + url
                    urllib2.urlopen(url3)
                    return url3
                except:
                    try:
                        url4 = "ftp://" + url
                        urllib2.urlopen(url4)
                        return url4
                    except:
                        return ""

    def start_new_download(self):
        if not self.urlBox.isChecked():
            self.download_with_one_url()
        else:
            self.download_with_two_urls()

    def download_with_one_url(self):
        NewFile = supervisor_api.Supervisor_manager_api()
        NewFile.set_url(self.check_url(self.get_url1()))
        NewFile.set_name_from_url()
        NewFile.set_parts(self.get_parts())
        NewFile.set_directory(self._get_directory_to_save())
        if NewFile.validate(download_choice_window_handler=self) == True:
            self.download_window_gui_handler = UI_dl()
            self.download_window_gui_handler.setGeometry(QtCore.QRect(500,500,400,300))
            self.download_window_gui_handler.show()
            # NewFile._set_file_download_list_handler(self.set_file_download_list_table)
            NewFile.main()
        else:
            pass


    def download_with_two_urls(self):
        NewFile = supervisor_api.Supervisor_manager_api()
        NewFile.set_url([self.check_url(self.get_url1()), self.check_url(self.get_url2())])
        NewFile.set_name_from_url()
        NewFile.set_parts(self.get_parts())
        NewFile.set_directory(self._get_directory_to_save())
        NewFile.set_slider_value(int(self.proportion_slider.value()))
        if NewFile.validate(download_choice_window_handler=self) == True:
            self.download_window_gui_handler = UI_dl()
            self.download_window_gui_handler.setGeometry(QtCore.QRect(500,500,400,300))
            self.download_window_gui_handler.show()
            # NewFile._set_file_download_list_handler(self.set_file_download_list_table)
            NewFile.set_file_download_list(self.file_download_list)
            NewFile.set_download_window_gui_handler(self.download_window_gui_handler)
            NewFile.main()


        else:
            pass