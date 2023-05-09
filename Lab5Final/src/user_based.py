import numpy as np
from numpy import ndarray
from pandas import DataFrame
import matplotlib.pyplot as plt

from util import *




def cal_pearson(utility_mat: DataFrame) -> DataFrame:
    """
    Calculate the pearson similarity matrix
    :param utility_mat:
    :return:
    """
    # Calculate the pearson similarity matrix
    return utility_mat.corr()


def find_k_sim(utility_mat :DataFrame,sim_mat: DataFrame, user: int, k: int = K) -> DataFrame:
    """
    Find the k most similar users to the user
    :param sim_mat:
    :param user:
    :param movie:
    :param k:
    :return:
    """

    # 找到K个最相似的用户
    # user = str(user)
    user = int(user)
    sim_dict = dict(sim_mat[user])
    # print(sim_dict)
    # 按照相似度排序
    sorted_sim_dict = sorted(sim_dict.items(), key=lambda x: x[1], reverse=True)
    # print(sorted_sim_dict)
    # top_k_id = [(sorted_sim_dict[i][0]) for i in range(k)]
    top_k_id = [str(sorted_sim_dict[i][0]) for i in range(k)]
    print(top_k_id)
    mat = utility_mat[top_k_id]
    return mat


def predict_k(utility_mat :DataFrame,sim_mat :DataFrame, user :int, movie: int, k :int = K) -> float:
    """
    Predict the rating of the movie by the user among the k most similar users
    :param top_k_mat:
    :param movie:
    :return: average rating among the k most similar users
    """
    top_k_mat = find_k_sim(utility_mat,sim_mat, user, k=k)
    # 获得 k 个最相似用户对 movie_id 的评分
    scores = top_k_mat.loc[str(movie)]
    # print(scores)
    pre_score = np.mean(scores[scores != 0])
    return pre_score


def recommand_n(utility_mat:DataFrame, sim_mat :DataFrame, user: int, k: int = K, n: int = N) -> list:
    """
    Recommend n movies for the user
    :param user:
    :param k: default 100
    :param n: default 10
    :return: list of movie ids
    """
    # 找到K个最相似的用户
    top_k_mat = find_k_sim(utility_mat, sim_mat, user, k)
    pred_dict = {}
    for i in range(len(utility_mat)):
        x = top_k_mat.iloc[i]
        if len(x[x != 0]) > 20:  # 某部电影至少有 20 个相关用户打过分才进行预测
            pred_i = np.mean(x[x != 0])
            pred_dict[i] = 0 if np.isnan(pred_i) else pred_i
        else:
            pred_dict[i] = 0
    sorted_pre_dict = sorted(pred_dict.items(), key=lambda x: x[1], reverse=True)
    # print(sorted_pre_dict)
    rec_list = [sorted_pre_dict[i][0] for i in range(n)]
    return rec_list


# define the test function
if __name__ == '__main__':
    # 根据训练集生成utility matrix
    utility_mat = generate_utility_mat()
    print(utility_mat)
    # 计算pearson相似度矩阵
    pearson_mat = cal_pearson(utility_mat)
    print(pearson_mat)
    # 找到与user K个最相似的用户
    top_k_mat = find_k_sim(utility_mat,pearson_mat, 1, k=10)
    print(top_k_mat)
    # 预测用户对电影movie的评分
    pre_score = predict_k(utility_mat, pearson_mat, 1, 1)
    print(pre_score)
    # 为每个用户推荐N个电影
    rec_list = recommand_n(utility_mat, pearson_mat, 10, K, n=10)
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
                pre_score = predict_k(utility_mat, pearson_mat, user, movie)
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
                    pre_score = predict_k(utility_mat, pearson_mat, user, movie, k=k)
                    sse += (pre_score - test_utility_mat[user][movie]) ** 2
        sse_list.append(sse)
    print(sse_list)
    plt.plot(k_list, sse_list)
    # save the figure
    plt.savefig(os.path.join(IMG_DIR, 'sse_minihash.png'))
    plt.show()


