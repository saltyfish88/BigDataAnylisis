import time
from utils import *
import numpy as np
from apriori import *


@timer
def pcy_generate_c1(data_set: list[list], hash_size: int = 100) -> tuple[set, list, list[list]]:
    """生成候选频繁一项集
    :param data_set: 数据集
    :return: 候选频繁一项集
    """
    c1 = set()
    hash_table = [0] * hash_size
    bucket = [[] for i in range(hash_size)]
    len1 = 0
    for basket in data_set:
        num = 0
        for item1 in basket:
            # frozenset:冻结集合，可以作为字典的key
            item = frozenset([item1])
            c1.add(item)
            num += 1
            # 生成hash表
        for i in range(len(basket)):
            for j in range(i+1,len(basket)):
                pair = frozenset([basket[i]]) | frozenset([basket[j]])
                str1 = ''.join(basket[i])
                str2 = ''.join(basket[j])
                str3 = str1 + str2
                # print(str3)
                hash_value = hash(str3) % hash_size
                # print(hash_value)
                hash_table[hash_value] += 1
                bucket[hash_value].append(pair)
        len1 += i**2/2
    print(len1)
    # 打印c1的长度
    # print("c1的长度为：", len(c1))

    # for i in range(hash_size):
    #     print((hash_table[i]))
    # print(sum(hash_table))
    return c1, hash_table, bucket

@timer
def pcy_generate_l1(data_set: list[list], ck: set[frozenset], hash_table,min_support, hash_size) \
        -> tuple[set[frozenset], dict[frozenset, float], list]:
    """
    根据 Ck 生成频繁 k 项集 L1
    :param data_set: 数据集
    :param ck: 候选频繁项集
    :param min_support: 最小支持度
    :return: 频繁 k 项集 Lk, 频繁项集支持度
    """
    # 字典，记录每个候选频繁项集出现的次数
    item_set_count = {}
    # 存储频繁桶的判断标准
    bitmap = [0] * hash_size
    # 频繁k项集
    lk = set()
    # 记录频繁项集的支持度
    fre_item_set_sup = {}
    for basket in data_set:
        for item_set in ck:
            if item_set.issubset(basket):
                # 统计候选频繁项集出现次数
                if item_set in item_set_count:
                    item_set_count[item_set] += 1
                else:
                    item_set_count[item_set] = 1
    data_num = len(data_set)
    print("data_num:", data_num)
    for key, value in item_set_count.items():
        # 计算支持度
        support = value / data_num
        if support >= min_support:
            lk.add(key)
            fre_item_set_sup[key] = support
    # print("频繁项集L1：", len(lk))
    # data_num = 3300/0.05
    print("data_num:", len(ck))
    data_num = 9835
    # 判断是否是频繁桶
    for i in range(hash_size):
        # 判断bucket是否大于支持度
        if hash_table[i] > min_support * data_num*2:
            bitmap[i] = 1
        else:
            bitmap[i] = 0

    return lk, fre_item_set_sup, bitmap


@timer
def pcy_generate_c2(lk: set[frozenset], k: int, bitmap, bucket) -> set[frozenset]:
    """
    根据 L2 构造候选频繁项集 C2
    :param lk: 频繁项集 Lk
    :param k: 频繁项集基数
    :return: 频繁候选项集 Ck+1
    """
    c2 = set()
    for i in range(max_hash_size):
        if (bitmap[i] == 1):  # 如果该桶是频繁的
            for item1 in bucket[i]:
                c2.add(item1)
    print("c2的长度为：", len(c2))
    return c2
