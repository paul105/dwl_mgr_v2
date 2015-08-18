#-*- coding: utf-8 -*-

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
def download_file(myFile):
    if myFile._set_size(myFile._get_size_from_url()) == 0:
            #todo downloading file with 1 part
            return "jakas_funkcja"

    process_pool = Pool(myFile.parts)
    myFile._set_data_block()
    myFile.prepare_temporary_files()
    for download_process_number in range(0,myFile.parts):
        start = download_process_number * int(myFile.data_block)
        if not download_process_number == myFile.parts -1:
            stop = start + int(myFile.data_block) -1
        else:
            stop = int(myFile.size)
        headers["Range"] = "bytes={}-{}".format(str(start),str(stop))
        request_object = urllib2.Request(myFile.url, headers=headers)
        process_pool.apply_async(func=downloader_file_manager.downloader,
                                 args=[download_process_number, request_object,
                                       myFile.temporary_directory])
    return process_pool

