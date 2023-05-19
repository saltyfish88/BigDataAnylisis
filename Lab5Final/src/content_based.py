from typing import Union

import numpy as np
from numpy import ndarray
from pandas import DataFrame
import matplotlib.pyplot as plt
from util import *
from config import *
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

movies = get_data('movies.csv')
tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(movies['genres'].tolist()).toarray()
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
utility_mat = generate_utility_mat()

# 电影id到索引的映射
index2id = dict(enumerate(movies['movieId']))
# 索引到id的映射
id2index = dict(zip(index2id.values(), index2id.keys()))


def predict(user: int, movie: int, k: int = K) -> Union[float, ndarray]:
    """
    Predict the rating of the movie by the user among the k most similar users
    :param user: user id
    :param movie: movie name
    :param k: the number of the most similar users
    :return: average rating among the k most similar users
    """
    user_id = str(user)
    movie = int(movie)
    # user = int(user)
    # 选取用户打分的电影
    user_movies = (utility_mat[user_id] != 0)
    # print("user_movies")
    # print(user_movies)
    rate = utility_mat[user_id][user_movies]
    # print("rate")
    # print(rate)
    # 获取电影的分值
    rated_score = np.array(rate.array)
    # print("rated_score")
    # print(rated_score)
    # 获得id集合
    movie_id = np.array(rate.index).astype(int)
    # print("movie_id")
    # print(movie_id)
    # 获得相似度
    dis = cosine_sim[id2index[int(movie)]]
    # print("distance")
    # print(dis)
    # 计算评分
    compute_score = {}
    for i in range(len(movie_id)):
        cos = dis[id2index[movie_id[i]]]
        if cos > 0:
            compute_score[i] = cos
    # 如果有相似的电影， 计算加权评分
    if len(compute_score) > 0:
        score_sum, sim_sum = 0, 0
        for k, v in compute_score.items():
            score_sum += rated_score[k] * v
            sim_sum += v
        return score_sum / sim_sum
    else:  # 计算集合为空，则计算平均值
        return np.mean(rated_score)


def recommend(user :int, n :int = N) -> list:
    user_id = str(user)
    user_movies = (utility_mat[user_id] != 0)
    rate = utility_mat[user_id][user_movies]
    # 获取电影的分值
    rated_score = np.array(rate.array)
    # 获得id集合
    movie_id = np.array(rate.index).astype(int)
    rec_list = {}
    # 遍历所有未打分电影并预测打分
    for i in range(len(movies)):
        idx = movies['movieId'][i]
        title = movies['title'][i]
        if idx not in movie_id:
            score = predict(user, idx)
            rec_list[(idx, title)] = score
    # 按照评分排序
    rec_list = sorted(rec_list.items(), key=lambda x: x[1], reverse=True)
    # 返回前n个
    return rec_list[:n]
    # 计算每个电影的相似度

# def the main function
if __name__ == '__main__':
    print("tfidf_matrix")
    print(tfidf_matrix)
    print(tfidf_matrix.shape)
    print("cosine_sim")
    print(cosine_sim)
    print(cosine_sim.shape)

    pre_score = predict(1, 1)
    print(pre_score)
    rec_list = recommend(1, n=10)
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
    # 计算测试集的sse
    sse = 0
    for user in test_utility_mat.columns:
        for movie in test_utility_mat.index:
            if test_utility_mat[user][movie] != 0:
                sse += (test_utility_mat[user][movie] - predict(user, movie)) ** 2
    print(sse)


