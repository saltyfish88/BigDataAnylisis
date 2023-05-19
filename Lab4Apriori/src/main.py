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
        # 存储每一行的数据
        row_data = row['items'].replace("{", "")
        row_data = row_data.replace("}", "")
        row_data = list(row_data.split(","))
        dataset.append(row_data)
    # print("dataset:", dataset)
    # 将dataset 写入文件
    with open(get_datafile('dataset'), 'w') as f:
        for item in dataset:
            f.write(str(item) + '\n')


    start = time.time()
    # # Apriori生成频繁项集
    # C1 = generate_c1(dataset)
    # L1, fre_item_set_sup1 = generate_lk(dataset, C1)
    # C2 = generate_next_ck(L1, 2)
    # print("C2:",len(C2))
    # L2, fre_item_set_sup2 = generate_lk(dataset, C2)
    # C3 = generate_next_ck(L2, 3)
    # L3, fre_item_set_sup3 = generate_lk(dataset, C3)
    # rules_list = generate_rules(
    #     L3, fre_item_set_sup1, fre_item_set_sup2, fre_item_set_sup3)
    # print("rules_list:", rules_list)


    # 加入PCY算法
    C1, hash_table, bucket = pcy_generate_c1(dataset, hash_size=max_hash_size)
    print("hash_table:", hash_table)
    # print(C1)
    L1, fre_item_set_sup1, bitmap = pcy_generate_l1(dataset, C1, hash_table, min_support=MIN_SUPPORT_OF_FREQ_ITEMS, hash_size=max_hash_size)
    # print(bitmap)
    # 存储bitmap值
    # with open(get_datafile('bitmap'), 'w') as f:
    #     i = 0
    #     for item in bitmap:
    #         f.write(str(item) + '  ')
    #         i += 1
    #         if i % 10 == 0: f.write('\n')
    C2 = pcy_generate_c2(L1, 2, bitmap, bucket)

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
    save_rules("rule", rules_list)

    print("1阶频繁项集个数为:", len(L1))
    print("2阶频繁项集个数为:", len(L2))
    print("3阶频繁项集个数为:", len(L3))
    print("关联规则个数为:", len(rules_list))
    print("用时:", end - start, 's')