#-*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
import urllib2
import os
import shutil
import time
import json

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

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name
        return self.name

    def set_name_from_url(self):
        try:
            if isinstance(self.url, str):
                self.name = self.url.split("/")[len(self.url.split("/")) - 1]
                return self.name
            elif isinstance(self.url, list):
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
        # try:
        #     return self.url
        # except:
        #     return self.url1, self.url2

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

    def validate(self, download_choice_window_handler):
        if len(self.url) == 1:
            if self.url[0] == '':
                QtGui.QMessageBox.about(download_choice_window_handler,"Error!","Nie wpisano adresu lub adres jest niepoprawny (serwer docelowy nie odpowiada)")
                return False
        elif len(self.url) == 2:
            if self.url[0] == '' or self.url[1] == '':
                QtGui.QMessageBox.about(download_choice_window_handler,"Error!","Nie wpisano adresu lub adres jest niepoprawny (serwer docelowy nie odpowiada)")
                return False

        if self.directory == '':
            QtGui.QMessageBox.about(download_choice_window_handler,"Error!","Nie wybrano katalogu lub katalog nie istnieje")
            return False

        if not isinstance(self.parts, int) or self.parts <= 0:
            QtGui.QMessageBox.about(download_choice_window_handler,"Error!","Nie wybrano ilosci czesci lub liczba jest niepoprawna")
            return False
        return True

    def compare_file_sizes(self):
        pass #TODO

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
        i=1
        while True:
            if os.path.exists(os.path.join(self.directory,self.name)):
                self.set_name('copy[{number}]_{file_name}'.format(number=str(i),
                                                                  file_name=self.name))
                i += 1
            else:
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



