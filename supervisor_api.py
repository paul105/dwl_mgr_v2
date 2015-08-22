#-*- coding: utf-8 -*-

import myFile_api
import downloader_file_manager
from multiprocessing import Manager, Process, Pool
import urllib2

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
        self.process_pool = Pool(self.parts)
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
            self.process_pool.apply_async(func=downloader_file_manager.downloader,
                                     args=[download_process_number, request_object,
                                           self.temporary_directory, self.child_dict])
        return self.process_pool

    def main(self):
        man = Manager()
        self.child_dict = man.dict()
        self.child_dict = {}
        self.set_size(self.get_size_from_url())
        if self.size == 0:
            self.downloader_unknown_size()
        else:
            self.downloader_one_url()
        self.process_pool.close()
        self.process_pool.join()
        self.delete_and_combine_parts()
        self.fileLogSave()






