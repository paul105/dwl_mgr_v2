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
                                           self.temporary_directory, self.child_dict])
        return self.process_pool

    def downloader_one_url(self):
        from threading import Thread
        # self.process_pool = Pool(self.parts)
        self.process_pool = []
        man = Manager()
        self.child_dict = man.dict()
        self.child_dict = {}

        self.set_data_block()
        self.prepare_temporary_files()
        for download_process_number in range(0, self.parts):
            start = download_process_number * int(self.data_block)
            if not download_process_number == self.parts -1:
                stop = start + int(self.data_block) -1
            else:
                stop = int(self.size)
            headers['Range'] = "bytes={}-{}".format(str(start),str(stop))
            request_object = urllib2.Request(self.url[0], headers=headers)
            thread = Thread(target=downloader_file_manager.downloader,
                            args=[download_process_number, request_object,
                                           self.temporary_directory, self.child_dict])
            thread.start()
            self.process_pool.insert(download_process_number,thread)
        return self.process_pool

    def set_text(self, number, part_number, s):
        divider = 1
        text = ('{:.2f}/{:.2f} ({:2.2f})% {:.2f} B/s'.format(
                    s/divider, self.data_block/divider,
                    ((s*100)/self.data_block), 0))
        try:
            data = float(self.child_dict[part_number]['data'])
            time = float(self.child_dict[part_number]['time'])
            speed = data/time
            if number == 0 :
                divider = 1
            elif number == 1:
                divider = 1024
            elif number == 2:
                divider = (1024**2)

            if speed/1024 > 1 and speed/(1024**2) < 0:
                text = ('{:.2f}/{:.2f} ({:2.2f})% {:.2f} KB/s'.format(
                    s/divider, self.data_block/divider,
                    ((s*100)/self.data_block), (speed/1024)
                ))
            elif speed/(1024**2) > 1:
                text = ('{:.2f}/{:.2f} ({:2.2f})% {:.2f} MB/s'.format(
                    s/divider, self.data_block/divider,
                    ((s*100)/self.data_block), (speed/(1024**2))
                ))
            else:
                text = ('{:.2f}/{:.2f} ({:2.2f})% {:.2f} B/s'.format(
                    s/divider, self.data_block/divider,
                    ((s*100)/self.data_block), speed
                ))
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
            for part_number in range(0, self.parts):
                suma += os.path.getsize(self.temporary_directory + "\\file" + str(part_number))
            if int(suma) == int(self.size):
                for part_number in range(0,self.parts):
                    self.process_pool[part_number].join()
                for part_number in range(0, self.parts):
                    s = float(os.path.getsize(self.temporary_directory + "\\file" + str(part_number)))
                    if s/1024 <0 :
                        text = self.set_text(0,part_number,s)
                    elif s/1024 > 1 and s/(1024**2) < 0 :
                        text = self.set_text(1,part_number,s)
                    elif s/(1024**2) > 1 :
                        text = self.set_text(2,part_number,s)
                    item = QtGui.QTableWidgetItem()
                    item.setText(text)
                    item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
                    ui_dl_handler.table_download_parts_info.setItem(part_number,0,item)
                # for part_number in range(0,self.parts):
                #     s = float(os.path.getsize(self.temporary_directory + "\\file" + str(part_number)))
                #     item = QtGui.QTableWidgetItem("%.2f/%.2f (100.00%%)" % (self.data_block/(1024**2), self.data_block/(1024**2)))
                #     item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
                #     ui_dl_handler.table_download_parts_info.setItem(part_number,0,item)
                self.delete_and_combine_parts()
                self.fileLogSave()
                self.set_file_download_list()
                ui_dl_handler.finish_button.setEnabled(True)
                break

            for part_number in range(0, self.parts):
                s = float(os.path.getsize(self.temporary_directory + "\\file" + str(part_number)))
                text = ''
                if s/1024 < 0 :
                    text = self.set_text(0,part_number,s)
                elif s/1024 > 1 and s/(1024**2) < 0 :
                    text = self.set_text(1,part_number,s)
                elif s/(1024**2) > 1 :
                    text = self.set_text(2,part_number,s)
                item = QtGui.QTableWidgetItem()
                item.setText(text)
                item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
                ui_dl_handler.table_download_parts_info.setItem(part_number,0,item)







