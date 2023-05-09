from content_based import *
from datasketch import MinHash, MinHashLSH


def generate_minihashsim_mat(tfidf_mat :DataFrame, num :int = NUM_HASH_FUNCS)-> DataFrame:
    """

    :param tfidf_mat:
    :return:
    """
    # Calculate the jarcard similarity matrix
    # 1. 计算每个用户的签名矩阵
    # 1.1. 初始化签名矩阵
    num_hash_funcs = num
    num_users = tfidf_mat.shape[0]
    print(num_users)
    signature_mat = []
    # 1.2. 计算签名矩阵
    for i in range(num_users):
        # 1.2.1. 生成 minihash,只要大于0的就是1
        m = MinHash(num_perm=num_hash_funcs)
        for j in range(tfidf_mat.shape[1]):
            if tfidf_mat[i][j] > 0:
                m.update(str(j).encode('utf-8'))
        # print(i)
        # 1.2.2. 生成签名矩阵
        signature_mat.append(m)
    print(signature_mat)
    # 2. 计算每个用户的签名矩阵的相似度
    # 2.1. 初始化相似度矩阵
    jaccard = np.zeros((num_users, num_users))
    # 2.2. 计算jaccard相似度矩阵
    for i in range(num_users):
        for j in range(i + 1, num_users):
            jaccard[i, j] = signature_mat[i].jaccard(signature_mat[j])
            jaccard[j, i] = jaccard[i, j]
    # # 3. 返回相似度矩阵,列名为1-671
    sim_mat = pd.DataFrame(jaccard).astype(float)
    return sim_mat


def predict_minihash(sim_mat :DataFrame, user: int, movie: int, k: int = K) -> float | ndarray:
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
    dis = sim_mat[id2index[int(movie)]]
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


def recommend_minihash(user :int, n :int = N) -> list:
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


# define the main function
if __name__ == '__main__':
    print(tfidf_matrix)
    sim_mat = generate_minihashsim_mat(tfidf_matrix)
    print(sim_mat)
    pre_score = predict_minihash(sim_mat, 1, 1)
    print(pre_score)
    rec_list = recommend_minihash(1)
    print(rec_list)

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

    # 使用不同的hash函数数量
    # 计算sse并画图
    hash_num = [i for i in range(10, 100, 5)]
    sse_list = []
    for num in hash_num:
        sim_mat = generate_minihashsim_mat(tfidf_matrix, num)
        sse = 0
        for user in test_utility_mat.columns:
            for movie in test_utility_mat.index:
                if test_utility_mat[user][movie] != 0:
                    sse += (test_utility_mat[user][movie] - predict(user, movie)) ** 2
        sse_list.append(sse)
    plt.plot(hash_num, sse_list)
    plt.xlabel('hash_num')
    plt.ylabel('sse')
    plt.show()
    plt.savefig(os.path.join(IMG_DIR, 'hash_num_sse.png'))


