# -*- coding: utf-8 -*-

"""
# @File       : mapper.py
# @Time       : 2023/4/14
# @Author     : EightHalf
# @Version    : Python 3.11.2
# @Description: implement the mapper
"""
import os
import threading
from util import *
import config


class Mapper(threading.Thread):
    def __init__(self, map_queue, map_node_num):
        threading.Thread.__init__(self)
        self.map_queue = map_queue
        self.map_node_num = map_node_num
        self.current_node_num = 0
        self.map_thread_list = []
        self.lock = threading.Lock()
        self.name = "Mapper"

    def read_file(self, file):
        """read the file
        :param file (TextIOWrapper): to be read
        :return(by yeild) str: the word
        """
        for line in file:
            line = line.strip()
            yield line.split(', ')
            # print(line)

    def mapper(self, src_file: str, dis_file: str) -> None:
        """write the map process results to file
        :param src_file: the file to be read
        :param dis_file: the file to be written
        :return None
        """
        file_read = open(src_file, 'r')
        file_write = open(dis_file, 'w')
        file_line = self.read_file(file_read)
        for words in file_line:
            for word in words:
                # write format: word, 1
                file_write.write("{},{}\n".format(word, 1))

    def join_thread(self):
        """join all the threads
        :return None
        """
        for thread in self.map_thread_list:
            thread.join()

    def create_map(self, idx: int):
        """create a map with idx
        :param idx: the idx of the map
        :return None
        """
        thread = create_thread(self.mapper, idx, "source0", "map")
        thread.start()
        thread.join()

    def run(self):
        print("Starting " + self.name)

        while self.current_node_num < self.map_node_num:
            pre_idx = self.current_node_num + 1
            thread = threading.Thread(target=self.create_map, args=(pre_idx,))
            self.map_thread_list.append(thread)
            thread.start()

            self.lock.acquire()
            self.current_node_num += 1
            self.lock.release()

        for i in range(self.map_node_num):
            self.map_queue.put(i)  # put the map idx into the queue
            self.map_thread_list[i].join()
        print("Exiting " + self.name)
