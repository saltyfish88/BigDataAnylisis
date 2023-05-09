import time
from utils import *
import numpy as np
from apriori import *


@timer
def pcy_generate_c1(data_set: list[list], hash_size: int = 100) -> tuple[set, list]:
    """生成候选频繁一项集
    :param data_set: 数据集
    :return: 候选频繁一项集
    """
    c1 = set()
    for basket in data_set:
        for item in basket:
            # frozenset:冻结集合，可以作为字典的key
            item = frozenset([item])
            c1.add(item)

        # add the pcy algorithm here
        hash_table = [0] * hash_size
        bucket = [[] for i in range(hash_size)]
        for item1 in c1:
            for item2 in c1:
                pair = item1 | item2
                str1 = ''.join(item1)
                str2 = ''.join(item2)
                str3 = str1 + str2
                if len(pair) == 2:
                    hash_value = hash(str(str3)) % hash_size
                    hash_table[hash_value] += 1
                    bucket[hash_value].append(pair)

    return c1, hash_table


def pcy_generate_l1(data_set: list[list], ck: set[frozenset], min_support, hash_table) \
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
    bitmap = [0] * max_hash_size
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
    for key, value in item_set_count.items():
        # 计算支持度
        support = value / data_num
        if support >= min_support:
            lk.add(key)
            fre_item_set_sup[key] = support

    # 判断是否是频繁桶
    for i in range(max_hash_size):
        if hash_table[i] >= MIN_SUPPORT_OF_FREQ_ITEMS:
            bitmap[i] = 1
    return lk, fre_item_set_sup, bitmap


@timer
def pcy_generate_c2(lk: set[frozenset], k: int, bitmap, hashtable) -> set[frozenset]:
    """
    根据 L2 构造候选频繁项集 C2
    :param lk: 频繁项集 Lk
    :param k: 频繁项集基数
    :return: 频繁候选项集 Ck+1
    """
    c2 = set()
    for i in range(max_hash_size):
        if (bitmap[i] == 1):  # 如果该桶是频繁的
            for item1 in hashtable[i]:
                c2.add(item1)
    return c2
