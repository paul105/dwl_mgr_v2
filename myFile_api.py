#-*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
import urllib2
import os

class MyFile(object):
    def __init__(self,name=None, urls=None, parts=None, directory=None, size=None):
#        self.temporary_directory = '{directory}\\TMP.{file_name}'.format(directory=self.directory, file_name= self.name)
        pass
        # self.name = name
        # try:
        #     if isinstance(urls,str):
        #         self.url = urls
        #     elif isinstance(urls,list):
        #         self.url1 = urls[0]
        #         self.url2 = urls[1]
        # except:
        #     raise "Wrong format of url"
        # self.parts = parts
        # self.directory = directory
        # if not size == None:
        #     self.size = size

    def _get_name(self):
        return self.name

    def _set_name(self, name):
        self.name = name
        return self.name

    def _set_name_from_url(self):
        try:
            self.name = self.url.split("/")[len(self.url.split("/")) - 1]
            return self.name
        except:
            self.name = self.url1.split("/")[len(self.url1.split("/")) - 1]
            return self.name

    def _get_directory(self):
        return self.directory

    def _set_directory(self, directory):
        self.directory = directory
        self._set_temporary_directory()
        return self.directory

    def _get_temporary_directory(self):
        return self.temporary_directory

    def _set_temporary_directory(self):
        self.temporary_directory = '{directory}\\TMP.{file_name}'.format(directory=self.directory, file_name=self.name)

    def _get_urls(self):
        try:
            return self.url
        except:
            return self.url1, self.url2

    def _set_urls(self, urls):
        try:
            if isinstance(urls,str):
                self.url = urls
            elif isinstance(urls,list):
                self.url1 = urls[0]
                self.url2 = urls[1]
        except:
            raise "Wrong format of url"

    def _get_parts(self):
        return self.parts

    def _set_parts(self, parts):
        self.parts = parts
        return self.parts

    def validate(self, download_choice_window_handler, one_url):
        if one_url == True:
            if self.url == '':
                QtGui.QMessageBox.about(download_choice_window_handler,"Error!","Nie wpisano adresu lub adres jest niepoprawny (serwer docelowy nie odpowiada)")
                return False
        elif one_url == False:
            if self.url1 == '' or self.url2 == '':
                QtGui.QMessageBox.about(download_choice_window_handler,"Error!","Nie wpisano adresu lub adres jest niepoprawny (serwer docelowy nie odpowiada)")
                return False

        if self.directory == '':
            QtGui.QMessageBox.about(download_choice_window_handler,"Error!","Nie wybrano katalogu lub katalog nie istnieje")
            return False

        if not isinstance(self.parts, int) or self.parts<= 0:
            QtGui.QMessageBox.about(download_choice_window_handler,"Error!","Nie wybrano ilosci czesci lub liczba jest niepoprawna")
            return False
        return True

    def compare_file_sizes(self):
        pass #TODO

    def _get_size_from_url(self):
        size = 0
        try:
            file_data = urllib2.urlopen(self.url)
            if file_data.headers['Accept-Ranges'] == 'bytes':
                if file_data.headers['Content-Length']:
                    size = file_data.headers['Content-Length']
        finally:
            return size


    def _set_size(self, size):
        self.size = size
        return size

    def prepare_temporary_files(self):
        try:
            os.mkdir(self.temporary_directory)
        except:
            pass
        for file_parts_number in range(0,self.parts):
            with open ('{}\\file{}'.format(self.temporary_directory, str(file_parts_number)), 'w+b') as file_part:
                pass

    def _set_data_block(self):
        self.data_block = float(self.size) / float(self.parts)
        return self.data_block





