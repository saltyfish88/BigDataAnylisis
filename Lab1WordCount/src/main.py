# -*- coding: utf-8 -*-

"""
# @File       : main.py
# @Time       : 2023/4/14
# @Author     : EightHalf
# @Version    : Python 3.11.2
# @Description: Lab1WordCount main file
"""
import time
import config
import queue
from mapper import Mapper
from combiner import Combiner
from shuffler import Shuffler
from reducer import Reducer
import os
import threading



def generate_subdict(file_name: str, sub_dict: dict) -> None:
    """生成子结果
    Args:
        file_name (str): reduce 结果的文件名
        sub_dict (dict): 子结果存放的字典名称
    """
    f_read = open(os.path.join(config.data_dir, file_name), 'r')
    for line in f_read:
        line = line.strip()
        word, count = line.split(',', 1)
        sub_dict[word] = count

def generate_result():
    """生成结果，保存在 res 目录下的 result 文件中
    """
    f_write = open(os.path.join(config.res_dir, 'result.csv'), 'w')

    sub_dict1 = {}
    sub_dict2 = {}
    sub_dict3 = {}
    sub_dict4 = {}

    t1 = threading.Thread(target=generate_subdict,
                          args=('reduce1', sub_dict1,))
    t1.start()
    t2 = threading.Thread(target=generate_subdict,
                          args=('reduce2', sub_dict2,))
    t2.start()
    t3 = threading.Thread(target=generate_subdict,
                          args=('reduce3', sub_dict3,))
    t3.start()

    # t4 = threading.Thread(target=generate_subdict,
    #                      args=('reduce4', sub_dict3,))
    # t4.start()

    t1.join()
    t2.join()
    t3.join()
    # t4.join()
    # 写入文件
    final_dict = {**sub_dict1, **sub_dict2, **sub_dict3}
    fin_list = sorted(final_dict.items(), key=lambda x: x[0])
    for key, value in fin_list:
        f_write.write("{},{}\n".format(key, value))

    print("Result has been generated in 'res' folder.")



if __name__ == '__main__':
    start_time = time.time()

    map_queue = queue.Queue(config.Map_Node_Num)
    combine_queue = queue.Queue(config.Combine_Node_Num)
    shuffle_queue = queue.Queue(config.Shuffle_Node_Num)
    reduce_queue = queue.Queue(config.Reduce_Node_Num)

    # 声明mapper、combiner、shuffler、reducer操作
    mapper = Mapper(map_queue=map_queue, map_node_num=config.Map_Node_Num)
    combiner = Combiner(combine_queue=combine_queue, combine_node_num=config.Combine_Node_Num)
    shuffler = Shuffler(combine_queue=combine_queue, shuffle_queue=shuffle_queue,
                        shuffle_node_num=config.Shuffle_Node_Num)
    reducer = Reducer(reduce_queue=reduce_queue, reduce_node_num=config.Reduce_Node_Num)
    # map，combine，shuffle操作并行处理
    mapper.start()
    combiner.start()
    shuffler.start()

    mapper.join()
    combiner.join()
    shuffler.join()
    # 以上三个操作执行完后，执行reduce操作
    reducer.start()
    reducer.join()
    #生成结果
    generate_result()



    print("All the process done.")
    end_time = time.time()
    print("Time cost: ", end_time - start_time)