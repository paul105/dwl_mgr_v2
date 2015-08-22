#-*- coding: utf-8 -*-
import urllib2
import time
import os
import shutil
import json


def downloader(i, req, dir, dict):               #funkcja dziecko, przekazujemy "id", "Request object", oraz katalog roboczy
    # a=0
    # if not req.has_header("Range"): a=1
    data = urllib2.urlopen(req)
    CHUNK = 1024*512                #ilosc danych czytana jednorazowo
    f_path = dir+"\\file"+str(i)
    with open(f_path,"wb") as output:
        while True:
            # __time_start = time.time()
            chunk = data.read(CHUNK)    #odczytujemy pobrana jednostke danych i zapisujemy, jak wszystko odczytane ->break
            # __time = time.time()-__time_start
            if not chunk:
                # if a == 1:
                #     del_and_combine(dir+"\\..", dir,str(dir).split(".",1)[1],1)
                break
            output.write(chunk)
            # CHUNK = int((CHUNK*0.3)+(len(chunk)/__time)*0.7)



def fileLogSave(name,url):
    with open("files","ab") as f:
        x = json.dumps({"name": str(name),"url": str(url), "date":time.strftime("%c")}, separators=(",",":"))
        f.write(x + "\n")