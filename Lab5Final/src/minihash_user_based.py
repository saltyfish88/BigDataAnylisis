from user_based import find_k_sim, predict_k, recommand_n, generate_utility_mat
import numpy as np
import pandas as pd
from datasketch import MinHash, MinHashLSH
from pandas import DataFrame
import matplotlib.pyplot as plt
from config import *


# minihash 使用jarcard相似度计算相似度矩阵
def generate_minihashsim_mat(utility_mat: DataFrame) -> DataFrame:
    """
    Calculate the jarcard similarity matrix
    :param utility_mat:
    :return:
    """
    # Calculate the jarcard similarity matrix
    # 1. 计算每个用户的签名矩阵
    # 1.1. 初始化签名矩阵
    num_hash_funcs = 10
    num_users = utility_mat.shape[1]
    signature_mat = []
    # 1.2. 计算签名矩阵
    for i in range(num_users):
        # 1.2.1. 生成 minihash,评分在0-5之间，0-2.5为0，2.5-5为1
        m = MinHash(num_perm=num_hash_funcs)
        for j in range(utility_mat.shape[0]):
            if utility_mat.iloc[j, i] > 2.5:
                m.update(str(j).encode('utf-8'))
        # 1.2.2. 生成签名矩阵
        signature_mat.append(m)
        # print(i)
    # print(signature_mat)
    # 2. 计算每个用户的签名矩阵的相似度
    # 2.1. 初始化相似度矩阵
    jaccard = np.zeros((num_users, num_users))
    # 2.2. 计算jaccard相似度矩阵
    for i in range(num_users):
        for j in range(i + 1, num_users):
            jaccard[i, j] = signature_mat[i].jaccard(signature_mat[j])
            jaccard[j, i] = jaccard[i, j]
    # # 3. 返回相似度矩阵,列名为1-671
    sim_mat = pd.DataFrame(jaccard, index=range(1, num_users + 1), columns=range(1, num_users + 1)).astype(float)
    return sim_mat


# define the main function
if __name__ == '__main__':
    utility_mat = generate_utility_mat()
    sim_mat = generate_minihashsim_mat(utility_mat)
    print(sim_mat)
    top_k = find_k_sim(utility_mat, sim_mat, user=1, k=100)
    pre_score = predict_k(utility_mat, sim_mat, user=1, movie=1, k=100)
    print(pre_score)
    rec_list = recommand_n(utility_mat, sim_mat, user=1, k=100, n=10)
    print(rec_list)

    # 评估推荐结果
    # 读取测试集
    test_file = open(os.path.join(DATA_DIR, 'test_set.csv'), 'r', encoding='utf-8')
    test_data = {}
    for line in test_file.readlines()[1:]:
        line = line.strip().split(',')
        if line[0] not in test_data.keys():
            test_data[line[0]] = {line[1]: line[2]}
        else:
            test_data[line[0]][line[1]] = line[2]
    # 生成测试集的utility matrix
    test_utility_mat = pd.DataFrame(test_data).fillna(0).astype(float)
    print(test_utility_mat)
    # 计算测试集的SSE
    sse = 0
    for user in test_utility_mat.columns:
        for movie in test_utility_mat.index:
            if test_utility_mat[user][movie] != 0:
                pre_score = predict_k(utility_mat, sim_mat, user, movie)
                sse += (pre_score - test_utility_mat[user][movie]) ** 2
    print(sse)
    # 计算RMSE
    rmse = np.sqrt(sse / len(test_utility_mat))
    print(rmse)
    # 画图显示SSE随K变化
    k_list = [i for i in range(50, 300, 10)]
    sse_list = []
    for k in k_list:
        sse = 0
        for user in test_utility_mat.columns:
            for movie in test_utility_mat.index:
                if test_utility_mat[user][movie] != 0:
                    pre_score = predict_k(utility_mat, sim_mat, user, movie, k=k)
                    sse += (pre_score - test_utility_mat[user][movie]) ** 2
        sse_list.append(sse)
    print(sse_list)
    plt.plot(k_list, sse_list)
    # save the figure
    plt.savefig(os.path.join(IMG_DIR, 'sse_hash.png'))
    plt.show()
