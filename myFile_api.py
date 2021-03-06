# -*- coding: utf-8 -*-
"""
:created on: '31/08/15'
:copyright: Paweł Nogieć
:author: Paweł Nogieć
:contact: nogiec.pawel@gmail.com
"""

from PyQt4 import QtGui, QtCore
import urllib2
import os
import shutil
import time
import json

class MyFile(object):
    def __init__(self,name=None, urls=None, parts=None, directory=None, size=None):
        pass

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name
        return self.name

    def set_name_from_url(self):
        try:
            self.name = self.url[0].split("/")[len(self.url[0].split("/")) - 1]
            return self.name
        except:
            pass

    def get_directory(self):
        return self.directory

    def set_directory(self, directory):
        self.directory = directory
        self.set_temporary_directory()
        return self.directory

    def get_temporary_directory(self):
        return self.temporary_directory

    def set_temporary_directory(self):
        self.temporary_directory = '{directory}\\TMP.{file_name}'.format(directory=self.directory, file_name=self.name)

    def get_url(self):
        return self.url

    def set_url(self, url):
        try:
            del self.url
        except:
            pass
        finally:
            if isinstance(url, str):
                self.url = [url]
            elif isinstance(url, list):
                self.url = url

        return self.url

    def get_parts(self):
        return self.parts

    def set_parts(self, parts):
        self.parts = parts
        return self.parts

    def set_slider_value(self,slider_value):
        self.slider_value = slider_value
        return self.slider_value

    def set_file_download_list(self,file_download_list):
        self.file_download_list = file_download_list
        return self.file_download_list

    def set_download_window_gui_handler(self, download_window_gui_handler):
        self.download_window_gui_handler = download_window_gui_handler
        return self.download_window_gui_handler

    def validate(self, download_choice_window_handler):
        if len(self.url) == 1:
            if self.url[0] == '':
                QtGui.QMessageBox.about(download_choice_window_handler,"Error!","Nie wpisano adresu lub adres jest niepoprawny (serwer docelowy nie odpowiada)")
                return False
        elif len(self.url) == 2:
            if self.url[0] == '' or self.url[1] == '':
                QtGui.QMessageBox.about(download_choice_window_handler,"Error!","Nie wpisano adresu lub adres jest niepoprawny (serwer docelowy nie odpowiada)")
                return False
            if not self.compare_file_sizes():
                QtGui.QMessageBox.about(download_choice_window_handler,"Error!","Pliki na podanych serwerach nie sa identyczne.")
                return False

        if self.directory == '':
            QtGui.QMessageBox.about(download_choice_window_handler,"Error!","Nie wybrano katalogu lub katalog nie istnieje")
            return False

        if not isinstance(self.parts, int) or self.parts <= 0:
            QtGui.QMessageBox.about(download_choice_window_handler,"Error!","Nie wybrano ilosci czesci lub liczba jest niepoprawna")
            return False
        return True

    def compare_file_sizes(self):
        size1 = None
        size2 = None
        try:
            file_data = urllib2.urlopen(self.url[0])
            if file_data.headers['Accept-Ranges'] == 'bytes':
                if file_data.headers['Content-Length']:
                    size1 = file_data.headers['Content-Length']
            file_data = urllib2.urlopen(self.url[1])
            if file_data.headers['Accept-Ranges'] == 'bytes':
                if file_data.headers['Content-Length']:
                    size2 = file_data.headers['Content-Length']
            if size1 == size2:
                return True
            else:
                return False
        except:
            return False



    def get_size_from_url(self):
        size = 0
        try:
            file_data = urllib2.urlopen(self.url[0])
            if file_data.headers['Accept-Ranges'] == 'bytes':
                if file_data.headers['Content-Length']:
                    size = file_data.headers['Content-Length']
        finally:
            return size


    def set_size(self, size):
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

    def set_data_block(self):
        self.data_block = float(self.size) / float(self.parts)
        return self.data_block

    def delete_and_combine_parts(self):
        i = 1
        if os.path.exists(os.path.join(self.directory,self.name)):
            while True:
                tmp_name = 'copy[{number}]_{file_name}'.format(number=str(i),
                                                           file_name=self.name)
                if os.path.exists(os.path.join(self.directory,tmp_name)):
                    i += 1
                else:
                    self.set_name(tmp_name)
                    break
        file_name = os.path.join(self.directory,self.name)
        with open(file_name, "wb") as downloaded_file:
            for i in range(0, self.parts):
                temporary_file_path = os.path.join(self.temporary_directory,'file{}'.format(str(i)))
                with open(temporary_file_path, "rb") as temporary_file:
                    while True:
                        try:
                            shutil.copyfileobj(temporary_file, downloaded_file)
                            break
                        except:
                            time.sleep(0.1)

        for i in range(0,self.parts):
            temporary_file_path = os.path.join(self.temporary_directory,'file{}'.format(str(i)))
            while True:
                try:
                    os.remove(temporary_file_path)
                    break
                except:
                    time.sleep(0.1)
        try:
            os.rmdir(self.temporary_directory)
        except:
            pass

    def fileLogSave(self):
        with open('files','ab') as file_log:
            if len(self.url) == 1:
                data_to_write = json.dumps({'name': str(self.name),'url1': str(self.url[0]),
                                            'url2' : '', 'date':time.strftime('%c')},
                                           separators=(',',':'))
            elif len(self.url) == 2:
                data_to_write = json.dumps({'name': str(self.name),'url1': str(self.url[0]),
                                            'url2' : str(self.url[1]), 'date':time.strftime('%c')},
                                           separators=(',',':'))
            file_log.write('{data}\n'.format(data=data_to_write))
