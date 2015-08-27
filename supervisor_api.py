#-*- coding: utf-8 -*-

import myFile_api
import downloader_file_manager
from multiprocessing import Manager, Process, Pool
import urllib2
from download_window_gui import UI_dl
from PyQt4 import QtGui, QtCore
import os

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "pl-PL,pl;q=0.8,en-US;q=0.6,en;q=0.4",
    "Connection": "keep-alive",
}
class Supervisor_manager_api(myFile_api.MyFile):
    # def __init__(self):
    #     super(UI_dl, self).__init__()

    def downloader_unknown_size(self):
        self.set_parts(1)
        self.process_pool = Pool(self.parts)
        try:
            del headers['Range']
        except:
            pass
        finally:
            if isinstance(self.url, str):
                request_object = urllib2.Request(self.url, headers=headers)
            elif isinstance(self.url, list):
                request_object = urllib2.Request(self.url[0], headers=headers)
            self.process_pool.apply_async(func=downloader_file_manager.downloader,
                                     args=[0, request_object,
                                           self.temporary_directory, self.manager_dictionary])
        return self.process_pool

    def downloader_one_url(self):
        from threading import Thread
        self.process_pool = []
        man = Manager()
        self.manager_dictionary = man.dict()
        self.manager_dictionary = {}
        for i in range(self.parts):
            self.manager_dictionary[i] = {
                'data'  : None,
                'time' : None,
                'time_start' : None,
                'time_stop' : None,
                'part_size' : None
            }

        self.set_data_block()
        self.prepare_temporary_files()
        for download_process_number in range(self.parts):
            start = download_process_number * int(self.data_block)
            if not download_process_number == self.parts -1:
                stop = start + int(self.data_block) -1
            else:
                stop = int(self.size)
            self.manager_dictionary[download_process_number]['part_size'] = int(stop-start)
            headers['Range'] = "bytes={}-{}".format(str(start),str(stop))
            request_object = urllib2.Request(self.url[0], headers=headers)
            thread = Thread(target=downloader_file_manager.downloader,
                            args=[download_process_number, request_object,
                                           self.temporary_directory, self.manager_dictionary])
            thread.start()
            self.process_pool.insert(download_process_number,thread)
        return self.process_pool

    def get_partial_file_size_and_set_text(self, part_number):
        actual_part_size = float(os.path.getsize(os.path.join(self.temporary_directory,'file{}'.format(part_number))))
        part_size = self.manager_dictionary[part_number]['part_size']
        if int(actual_part_size) >= self.manager_dictionary[part_number]['part_size']-1:
            self.manager_dictionary[part_number]['data'] = 0.0
            self.manager_dictionary[part_number]['time'] = 1.0


        if part_size/1024 <0 :
            return self.set_text(1,part_number,actual_part_size)
        elif 1000 > part_size/1024 > 1:
            return self.set_text(2,part_number,actual_part_size)
        elif part_size/(1024**2) > 1 :
            return self.set_text(3,part_number,actual_part_size)
        else:
            return "ala ma kota"

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
                    actual_part_size/divider, self.data_block/divider,
                    (actual_part_size*100)/self.data_block, speed))

            elif number == 2:
                divider = 1024
                text = ('{:.2f}/{:.2f} ({:2.2f}%)   {:.2f} KB/s'.format(
                    actual_part_size/divider, self.data_block/divider,
                    (actual_part_size*100)/self.data_block, speed/divider))

            elif number == 3:
                divider = (1024**2)
                text = ('{:.2f}/{:.2f} ({:2.2f}%)   {:.2f} MB/s'.format(
                    actual_part_size/divider, self.data_block/divider,
                    (actual_part_size*100)/self.data_block, speed/divider))
        except:
            pass
        finally:
            return text


    def main(self, ui_dl_handler):

        self.set_size(self.get_size_from_url())
        if self.size == 0:
            self.downloader_unknown_size()
        else:
            self.downloader_one_url()
        ui_dl_handler.set_table_download_parts_info_rows(self.parts)

        while True:
            QtCore.QCoreApplication.processEvents()
            suma = 0
            for part_number in range(self.parts):
                suma += os.path.getsize(os.path.join(self.temporary_directory,'file{}'.format(part_number)))
            if int(suma) == int(self.size):
                [self.process_pool[part_number].join() for part_number in range(self.parts)]
                for part_number in range(self.parts):
                    text = self.get_partial_file_size_and_set_text(part_number)
                    item = QtGui.QTableWidgetItem()
                    item.setText(text)
                    item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
                    ui_dl_handler.table_download_parts_info.setItem(part_number,0,item)
                self.delete_and_combine_parts()
                self.fileLogSave()
                self.set_file_download_list()
                ui_dl_handler.finish_button.setEnabled(True)
                break

            for part_number in range(self.parts):
                text = self.get_partial_file_size_and_set_text(part_number)
                item = QtGui.QTableWidgetItem()
                item.setText(text)
                item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
                ui_dl_handler.table_download_parts_info.setItem(part_number,0,item)







