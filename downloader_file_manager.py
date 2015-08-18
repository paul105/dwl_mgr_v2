#-*- coding: utf-8 -*-
import urllib2
import time
import os
import shutil
import json


def downloader(i, req, dir):               #funkcja dziecko, przekazujemy "id", "Request object", oraz katalog roboczy
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

def del_and_combine(dir,dir_tmp,f_name,N):
    file = dir + "\\" + f_name
    i=1

    while True:
        if os.path.exists(file):
            try:
                os.remove(file)
                break
            except:
                file = dir + "\\copy[" + str(i) + "]_" + f_name
                i=i+1
        else:
            break
    with open(file, "wb") as of:
        for i in range(0, N):
            f_path = dir_tmp + "\\file" + str(i)
            with open(f_path, "rb") as f:
                shutil.copyfileobj(f, of)
            while True:
                try:
                    os.remove(f_path)
                    break
                except:
                    pass
        while True:
            try:
                os.rmdir(dir_tmp)
                break
            except:
                pass

def fileLogSave(name,url):
    with open("files","ab") as f:
        x = json.dumps({"name": str(name),"url": str(url), "date":time.strftime("%c")}, separators=(",",":"))
        f.write(x + "\n")