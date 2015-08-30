#-*- coding: utf-8 -*-

import myFile_api
import downloader_file_manager
from multiprocessing import Manager, Process, Pool
import urllib2
from download_window_gui import UI_dl
from PyQt4 import QtGui, QtCore
import os
from threading import Thread

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "pl-PL,pl;q=0.8,en-US;q=0.6,en;q=0.4",
    "Connection": "keep-alive",
}
class Supervisor_manager_api(myFile_api.MyFile):

    def downloader_unknown_size(self):
        self.set_parts(1)
        self.set_manager_dictionary()
        try:
            del headers['Range']
        except:
            pass
        finally:
            request_object = urllib2.Request(self.url[0], headers=headers)
            self.threads_pool = [Thread(target=downloader_file_manager.downloader,
                                     args=[0, request_object,
                                           self.temporary_directory, self.manager_dictionary])]
            return self.threads_pool

    def downloader_one_url(self):
        self.set_manager_dictionary()
        self.set_data_block()
        self.prepare_temporary_files()
        request_object_list = self._set_request_object()
        self.threads_pool = self._start_new_threads(request_object_list)
        return self.threads_pool

    def downloader_two_url(self, slider_value): ###############################################
        self.set_manager_dictionary()
        self.prepare_temporary_files()
        self.threads_pool = []
        size1 = int(int(self.size)*slider_value)
        print slider_value
        print size1
        size2 = int(self.size)-int(size1)
        print size2
        print size1+size2
        checker = float(self.parts)*slider_value
        checker_int = None
        if 0.5 > checker > 0:
            checker_int = 1
        elif self.parts > checker > self.parts-(0.5):
            checker_int = int(self.parts) -1
        else:
            checker_int = int(round(checker))
        if checker_int == 0:
            self.set_data_block()
            request_object_list = self._set_request_object(url=False)
            self.threads_pool = self._start_new_threads(request_object_list)
        elif checker_int == self.parts:
            self.set_data_block()
            request_object_list = self._set_request_object()
            self.threads_pool = self._start_new_threads(request_object_list)
        elif self.parts > checker_int > 0: #checker_int < checker or checker_int > checker or checker_int == checker:
            parts = self.parts
            self.set_size(int(size1)-1)
            self.set_parts(checker_int)
            self.set_data_block()
            request_object_list = self._set_request_object()
            self.threads_pool = self._start_new_threads(request_object_list)  ###todo cos

            self.set_parts(int(parts)-checker_int)
            print "parts = ", self.parts
            self.set_size(size2)
            print "size2 = ", self.size
            self.set_data_block()
            print "data_block2 = ", self.data_block
            self.set_parts(parts)
            print "parts later = ", self.parts
            request_object_list += self._set_request_object(begin=checker_int, url=False, size1=size1)
            self.threads_pool += self._start_new_threads(request_object_list, begin=checker_int)
            self.set_size(size1+size2)
        return self.threads_pool


    def _start_new_threads(self, request_object_list, begin=0):
        threads_pool = []
        for download_process_number in range(begin, self.parts):
            thread = Thread(target=downloader_file_manager.downloader,
                            args=[download_process_number, request_object_list[download_process_number],
                                           self.temporary_directory, self.manager_dictionary])
            thread.start()
            threads_pool.append(thread)
        return threads_pool

    def _set_request_object(self, begin=0, url=True, size1=0):
        if url:
            url = self.url[0]
        else:
            url = self.url[1]
        request_object_list = []
        for download_process_number in range(begin, self.parts):

            start = (download_process_number-begin) * int(self.data_block) + size1
            stop=0
            if not download_process_number == self.parts -1:
                stop = start + int(self.data_block) -1
            else:
                stop = int(self.size) + size1
            print "process number = {}, start = {}, stop = {}, part_size = {}".format(download_process_number, start, stop, stop-start)
            self.manager_dictionary[download_process_number]['part_size'] = int(stop-start)
            headers['Range'] = "bytes={}-{}".format(str(start),str(stop))
            request_object_list.append(urllib2.Request(url, headers=headers))
        return request_object_list

    def get_partial_file_size_and_set_text(self, part_number):
        actual_part_size = float(os.path.getsize(os.path.join(self.temporary_directory,'file{}'.format(part_number))))
        part_size = self.manager_dictionary[part_number]['part_size']
        if int(actual_part_size) >= self.manager_dictionary[part_number]['part_size']-1:
            self.manager_dictionary[part_number]['data'] = 0.0
            self.manager_dictionary[part_number]['time'] = 1.0
        # print "actial = ", actual_part_size
        # print "part = ", part_size
        if float(part_size)/1024 <0 :
            return self.set_text(1,part_number,actual_part_size)
        elif 1000 > float(part_size)/1024 > 1:
            return self.set_text(2,part_number,actual_part_size)
        elif float(part_size)/(1024*1024) > 1 :
            return self.set_text(3,part_number,actual_part_size)
        else:
            return str(part_size)

    def set_text(self, number, part_number, actual_part_size):
        text = ('{:.2f}/{:.2f} ({:2.2f}%)   {:.2f} B/s'.format(
                    actual_part_size, self.data_block,
                    (actual_part_size*100)/self.data_block, 0))
        try:
            data = float(self.manager_dictionary[part_number]['data'])
            time = float(self.manager_dictionary[part_number]['time'])
            speed = data/time
            if number == 1 :
                divider = 1
                text = ('{:.2f}/{:.2f} ({:2.2f}%)   {:.2f} B/s'.format(
                    actual_part_size/divider, float(self.manager_dictionary[part_number]['part_size'])/divider,
                    (actual_part_size*100)/float(self.manager_dictionary[part_number]['part_size']), speed))

            elif number == 2:
                divider = 1024
                text = ('{:.2f}/{:.2f} ({:2.2f}%)   {:.2f} KB/s'.format(
                    actual_part_size/divider, float(self.manager_dictionary[part_number]['part_size'])/divider,
                    (actual_part_size*100)/float(self.manager_dictionary[part_number]['part_size']), speed/divider))

            elif number == 3:
                divider = (1024**2)
                text = ('{:.2f}/{:.2f} ({:2.2f}%)   {:.2f} MB/s'.format(
                    actual_part_size/divider, float(self.manager_dictionary[part_number]['part_size'])/divider,
                    (actual_part_size*100)/float(self.manager_dictionary[part_number]['part_size']), speed/divider))
            else:
                text = "ala ma kota"
        except:
            pass
        finally:
            return text

    def set_manager_dictionary(self):
        for i in range(self.parts):
            self.manager_dictionary[i] = {
                'data'  : None,
                'time' : None,
                'time_start' : None,
                'time_stop' : None,
                'part_size' : None
            }

    def main(self, ui_dl_handler, slider_value=None):
        self.set_size(self.get_size_from_url())
        man = Manager()
        self.manager_dictionary = man.dict()
        self.manager_dictionary = {}

        if self.size == 0:
            self.downloader_unknown_size()
        elif self.size !=0 and len(self.url) == 1:
            self.downloader_one_url()
        elif self.size !=0 and len(self.url) == 2:
            self.downloader_two_url(slider_value*0.01)
        ui_dl_handler.set_table_download_parts_info_rows(self.parts)

        while True:
            QtCore.QCoreApplication.processEvents()
            suma = 0
            for part_number in range(self.parts):
                suma += os.path.getsize(os.path.join(self.temporary_directory,'file{}'.format(part_number)))
            if int(suma) == int(self.size):
                [self.threads_pool[part_number].join() for part_number in range(self.parts)]
                for part_number in range(self.parts):
                    text = self.get_partial_file_size_and_set_text(part_number)
                    item = QtGui.QTableWidgetItem()
                    item.setText(text)
                    item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
                    ui_dl_handler.table_download_parts_info.setItem(part_number,0,item)
                self.delete_and_combine_parts()
                self.fileLogSave()
                self._set_file_download_list_handler()
                ui_dl_handler.finish_button.setEnabled(True)
                break

            for part_number in range(self.parts):
                text = self.get_partial_file_size_and_set_text(part_number)
                item = QtGui.QTableWidgetItem()
                item.setText(text)
                item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
                ui_dl_handler.table_download_parts_info.setItem(part_number,0,item)







