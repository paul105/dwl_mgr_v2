import supervisor_api
import os
import multiprocessing
import urllib2
from threading import Thread
import downloader_file_manager

headers = {}
# man_dict = {0: {}}

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
        # self.manager_dictionary[download_process_number]['part_size'] = int(stop-start)
        headers['Range'] = "bytes={}-{}".format(str(start),str(stop))
        request_object_list.append(urllib2.Request(url, headers=headers))
    return request_object_list

def start_new_threads(self, request_object_list, man_dict, tmp_dict, begin=0):
        threads_pool = []
        for download_process_number in range(begin, self.parts):
            thread = Thread(target=downloader_file_manager.downloader,
                            args=[download_process_number, request_object_list[download_process_number],
                                  tmp_dict, man_dict])
            thread.start()
            threads_pool.append(thread)
        return threads_pool

def main(man_dict, part):
    path = "D:\\userdata\\nogiec\\Desktop"
    file = supervisor_api.Supervisor_manager_api()
    file.set_url("http://pluton.kt.agh.edu.pl/~pnogiec/100M")
    file.set_name_from_url()
    file.set_parts(part)
    file.set_directory(path)
    file.set_size(file.get_size_from_url())
    file.set_data_block()
    file.prepare_temporary_files()
    tmp_dict = file.temporary_directory
    request_object_list = _set_request_object(file)
    threads_pool = start_new_threads(file, request_object_list, man_dict, tmp_dict)
    for thread in threads_pool:
        thread.join()
    file.delete_and_combine_parts()

if __name__ == '__main__':
    multiprocessing.freeze_support()
    man_dict = {0: {}}
    for _ in xrange(1,3):

        man_dict.update({int(_): {}})
        print man_dict
        main(man_dict, _)