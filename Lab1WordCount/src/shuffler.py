import os
import threading
import config
from util import *
import hashlib




class Shuffler(threading.Thread):
    def __init__(self, combine_queue,shuffle_queue, shuffle_node_num):
        threading.Thread.__init__(self)
        self.combine_queue = combine_queue
        self.shuffle_queue = shuffle_queue
        self.shuffle_node_num = shuffle_node_num
        self.current_node_num = 0
        self.shuffle_thread_list = []
        self.lock = threading.Lock()
        self.name = "Shuffler"

    def hash_str_3(self, word) -> int:
        if 97 <= ord(word) <= 105 or 65 <= ord(word) <= 73:  # a(A) 到 i(I)
            return 1
        elif 106 <= ord(word) <= 114 or 74 <= ord(word) <= 82:  # j(J) 到 r(R)
            return 2
        else:
            return 3

    def hash_str_4(self, word) -> int:
        if 97 <= ord(word) <= 103 or 65 <= ord(word) <= 70:
            return 1
        elif 104 <= ord(word) <= 109 or 71 <= ord(word) <= 76:
            return 2
        elif 110 <= ord(word) <= 115 or 77 <= ord(word) <= 82:
            return 3
        else:
            return 4

    def shuffler(self, src_file: str, dis_file: str) -> None:
        """write the map process results to file
        :param src_file: the file to be read
        :param dis_file: the file to be written
        :return None
        """
        file_read = open(src_file, 'r')

        for line in file_read:
            # print(line)
            line = line.strip()
            word, count = line.split(',', 1)
            idx = self.hash_str_3(word[0])
            file_write = open(dis_file+str(idx),'a')
            file_write.write("{},{}\n".format(word, count))

    def create_shuffle(self, idx):
            """
            :param idx:
            :return:
            """
            print("Creating combine node: ", idx)
            thread = create_thread(target=self.shuffler,idx=idx, src_str="combine",dis_str="shuffle")
            thread.start()
            thread.join()

    def run(self) -> None:

        print("Starting " + self.name)
        while self.current_node_num < self.shuffle_node_num:
            queue = self.combine_queue.get()
            if queue:
                idx = int(queue)
                thread = threading.Thread(
                    target=self.create_shuffle, args=(idx,)
                )
                self.shuffle_thread_list.append(thread)
                thread.start()

                self.lock.acquire()
                self.current_node_num += 1
                self.lock.release()

        for i in range(self.shuffle_node_num):
            self.shuffle_thread_list[i].join()
            self.shuffle_queue.put(i)

        print("Exiting " + self.name)


