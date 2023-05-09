import os
import threading
import config
from util import *
import hashlib

class Reducer(threading.Thread):
    def __init__(self, reduce_queue, reduce_node_num):
        threading.Thread.__init__(self)
        self.reduce_queue = reduce_queue
        self.reduce_node_num = reduce_node_num
        self.current_node_num = 0
        self.reduce_thread_list = []
        self.lock = threading.Lock()
        self.name = "Reducer"

    def reducer(self, src_file: str, dis_file: str) -> None:
        """进行reduce操作
        :param src_file: the file to be read
        :param dis_file: the file to be written
        :return None
        """
        f_read = open(src_file, 'r')
        f_write = open(dis_file, 'w')
        count_dict = {}
        # 同 combine操作几倍类似
        for line in f_read:
            line = line.strip()
            word, count = line.split(',', 1)
            # 将count转换为int类型，如果不能转换则跳过，目的是过滤掉不合法的数据
            try:
                count = int(count)
            except ValueError:
                continue
            if word in count_dict.keys():
                count_dict[word] += count
            else:
                count_dict[word] = count
        # 按照字典的键排序，目的是方便生成结果
        count_dict = sorted(
            count_dict.items(), key=lambda x: x[0], reverse=False)
        # 写入文件，格式为：word, count
        for k, v in count_dict:
            f_write.write("{},{}\n".format(k, v))

    def create_reduce(self, idx):
        """
        :param idx:
        :return:
        """
        thread = create_thread(target=self.reducer,idx=idx, src_str="shuffle",dis_str="reduce")
        thread.start()
        thread.join()


    def run(self):
        """run the reduce process
        :return None
        """
        print("Starting " + self.name)
        while self.current_node_num < self.reduce_node_num:
            idx = self.current_node_num + 1
            thread = threading.Thread(
                target=self.create_reduce, args=(idx,))
            self.reduce_thread_list.append(thread)
            thread.start()
            self.lock.acquire()
            self.current_node_num += 1
            self.lock.release()

        for i in range(self.reduce_node_num):
            self.reduce_thread_list[i].join()
            self.reduce_queue.put(i)

        print("Exiting " + self.name)


