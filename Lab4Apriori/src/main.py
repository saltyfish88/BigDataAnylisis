import pandas as pd
import numpy as np
from apriori import *
from pcy import *


if __name__ == '__main__':
    start = time.time()
    # 数据读取
    dataset = []
    data = pd.read_csv(get_datafile('Groceries.csv'), header=0)
    for _, row in data.iterrows():
        row_data = row['items'].replace("{", "")
        row_data = row_data.replace("}", "")
        row_data = list(row_data.split(","))
        dataset.append(row_data)

    # # Apriori生成频繁项集
    # C1 = generate_c1(dataset)
    # L1, fre_item_set_sup1 = generate_lk(dataset, C1)
    # C2 = generate_next_ck(L1, 2)
    # L2, fre_item_set_sup2 = generate_lk(dataset, C2)
    # C3 = generate_next_ck(L2, 3)
    # L3, fre_item_set_sup3 = generate_lk(dataset, C3)
    # rules_list = generate_rules(
    #     L3, fre_item_set_sup1, fre_item_set_sup2, fre_item_set_sup3)
    # end = time.time()

    start = time.time()
    # 加入PCY算法
    hash_table, C1 = pcy_generate_c1(dataset, hash_size=max_hash_size)
    # print("hash_table:", hash_table)
    L1, fre_item_set_sup1, bitmap = pcy_generate_l1(dataset, C1, hash_table)
    C2 = pcy_generate_c2(L1, 2, bitmap, hash_table)
    L2, fre_item_set_sup2 = generate_lk(dataset, C2)
    C3 = generate_next_ck(L2, 3)
    L3, fre_item_set_sup3 = generate_lk(dataset, C3)
    rules_list = generate_rules(
        L3, fre_item_set_sup1, fre_item_set_sup2, fre_item_set_sup3)
    end = time.time()


    # 保存结果
    save_fre_item_set("L1.csv", fre_item_set_sup1)
    save_fre_item_set("L2.csv", fre_item_set_sup2)
    save_fre_item_set("L3.csv", fre_item_set_sup3)
    # save_rules("rule", rules_list)

    print("1阶频繁项集个数为:", len(L1))
    print("2阶频繁项集个数为:", len(L2))
    print("3阶频繁项集个数为:", len(L3))
    print("关联规则个数为:", len(rules_list))
    print("用时:", end - start, 's')