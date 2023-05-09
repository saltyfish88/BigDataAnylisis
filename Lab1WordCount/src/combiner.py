# -*- coding: utf-8 -*-

"""
# @File       : combiner.py
# @Time       : 2022/11/24
# @Author     : Asuna
# @Version    : Python 3.11
# @Description: 实现 combine 功能
"""
from util import *


class Combiner(threading.Thread):
    def __init__(self, combine_queue, combine_node_num):
        threading.Thread.__init__(self)
        self.combine_queue = combine_queue
        self.combine_node_num = combine_node_num
        self.current_node_num = 0
        self.combine_thread_list = []
        self.lock = threading.Lock()
        self.name = "Combiner"

    def combiner(self, src_file: str, dis_file: str) -> None:
        """write the map process results to file
        :param src_file: the file to be read
        :param dis_file: the file to be written
        :return None
        """
        # 读取文件
        file_read = open(src_file, 'r')
        file_write = open(dis_file, 'w')
        word_dict = {}
        # 读取文件的每一行
        for line in file_read:
            # print(line)
            line = line.strip()
            word, count = line.split(',')
            # 使用字典存储单词和出现次数
            if word not in word_dict.keys():
                word_dict[word] = int(count)
            else:
                word_dict[word] += int(count)
        # 按照字典的键排序， 目的是为了方便后续的reduce
        word_dict = sorted(word_dict.items(), key=lambda x: x[0])
        # 写入combine-x文件中，格式为：word, count
        for word, count in word_dict:
            file_write.write("{},{}\n".format(word, count))

    def create_combine(self, idx: int):
        """create a combine with idx
        :param idx: the idx of the map
        :return None
        """
        # print("Creating combine node: ", idx)
        thread = create_thread(target=self.combiner, idx=idx, src_str="map", dis_str="combine")
        thread.start()
        thread.join()

    def run(self):
        """run the combine process
        :return None
        """
        print("Starting " + self.name)
        while self.current_node_num < self.combine_node_num:
            idx = self.current_node_num + 1
            thread = threading.Thread(
                target=self.create_combine, args=(idx,))
            self.combine_thread_list.append(thread)
            thread.start()
            self.lock.acquire()
            self.current_node_num += 1
            self.lock.release()

        for i in range(self.combine_node_num):
            self.combine_thread_list[i].join()
            self.combine_queue.put(i)

        print("Exiting " + self.name)
