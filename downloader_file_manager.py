# -*- coding: utf-8 -*-
"""
:created on: '31/08/15'
:copyright: Paweł Nogieć
:author: Paweł Nogieć
:contact: nogiec.pawel@gmail.com
"""

import urllib2
import time
import os
import shutil
import json


def downloader(child_number, request_object, temporary_directory, manager_dictionary):
    manager_dictionary[child_number]['time_start']  = time.time()
    # a=0
    # if not req.has_header("Range"): a=1
    data = urllib2.urlopen(request_object)
    CHUNK = 1024*512                #ilosc danych czytana jednorazowo
    f_path = temporary_directory+"\\file"+str(child_number)
    with open(f_path,"wb") as output:
        while True:
            _time_start = time.time()
            chunk = data.read(CHUNK)    #odczytujemy pobrana jednostke danych i zapisujemy, jak wszystko odczytane ->break
            _time = time.time()-_time_start
            if not chunk:
                manager_dictionary['time_stop'] = time.time()
                # if a == 1:
                #     del_and_combine(dir+"\\..", dir,str(dir).split(".",1)[1],1)
                break
            output.write(chunk)
            manager_dictionary[child_number]['data'] = CHUNK
            manager_dictionary[child_number]['time'] = _time
            # print 'Child {}, CHUNK = {}, time = {}'.format(child_number, CHUNK, _time)
            try:
                CHUNK = int((CHUNK*0.3)+(len(chunk)/_time)*0.7)
            except:
                pass




def fileLogSave(name,url):
    with open("files","ab") as f:
        x = json.dumps({"name": str(name),"url": str(url), "date":time.strftime("%c")}, separators=(",",":"))
        f.write(x + "\n")