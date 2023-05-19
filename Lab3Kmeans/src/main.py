import matplotlib.pyplot as plt
from config import *
import numpy as np
import pandas as pd

# 画图设置
plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置字体
plt.rcParams["axes.unicode_minus"] = False  # 该语句解决图像中的“-”负号的乱码问题




def data_preprocess(file_path: str) -> tuple[pd.DataFrame, pd.DataFrame, int]:
    """
    数据预处理
    :param data_path: 数据路径
    :return: 数据集
    """
    # 类 1: 59
    # 类 2: 71
    # 类 3: 48
    # 读取数据 (13个特征)
    data = pd.read_csv(os.path.join(data_dir, file_path), header=None)
    # 数据归一化
    # data = (data - data.min()) / (data.max() - data.min())
    print(data.head())
    # 去掉第一行的类别
    return data[0], data.drop([0], axis=1), len(data)
    # return data[0], data, len(data)

def cal_sse(mat: np.mat, length: int, k: int = 3) -> float:
    """
    计算sse
    :param mat: 数据集
    :param length: 数据集长度
    :param k: 聚类中心个数
    :return: sse
    """
    sse_num = np.zeros(3)
    sse = 0
    for i in range(length):
        type = int(mat[i, 1]) - 1
        sse_num[type] += mat[i, 0]
    sse += sum(sse_num)
    print("All sse: ", sse)
    return sse


def gen_rand_ceter(data: pd.DataFrame, length: int, k: int = 3) -> np.ndarray:
    """
    生成随机聚类中心
    :param data: 数据集
    :param length: 数据集长度
    :return: 聚类中心
    """
    data_list = data.to_numpy()
    rand_ceter = np.zeros((k, data.shape[1]))
    # 随机生成聚类中心
    # for j in range(data.shape[1]):
    #     rand_ceter[:, j] = np.random.rand(k)
    # 缩小范围生成聚类中心
    for j in range(data.shape[1]):
        # 获取每一列的最小值和最大值
        ran = float(max(data_list[:, j]) - min(data_list[:, j]))
        # 设置随机种子
        rand_ceter[:, j] = min(data_list[:, j]) + ran * np.random.rand(k)
    return rand_ceter


def gen_acc(mat: np.mat, length: int, k: int = 3) -> float:
    """
    计算准确率
    :param mat: 数据集
    :param length: 数据集长度
    :param k: 聚类中心个数
    :return: 准确率
    """
    acc = 0
    for i in range(length):
        if mat[i, 1] == mat[i, 2]:
            acc += 1
    print("acc: ", acc / length)
    return acc / length


if __name__ == "__main__":
    label,data, length = data_preprocess("归一化数据.csv")
    # 初始化聚类中心个数
    k = cluster_num
    # 初始化最大迭代次数
    iter_num = max_iter
    # 矩阵，第一列存储欧式距离，第二列存储类别，第三列存储真实类别
    mat = np.mat(np.zeros((length, 3)))
    # 初始化真实类别
    for i in range(length):
        if i < 59:
            mat[i, 2] = 1
        elif i < 130:
            mat[i, 2] = 2
        else:
            mat[i, 2] = 3
    # print(label)
    #print(mat)
    # 初始化聚类中心
    cluster_centers = gen_rand_ceter(data, length, k)
    #print(cluster_centers)
    sse_list = []
    # 迭代
    for i in range(iter_num):
        print("iter: ", i)
        # 计算欧式距离
        for j in range(length):
            min_dist = np.inf
            min_index = -1
            # 完成分类
            for l in range(k):
                # 计算欧式距离
                dist = np.sqrt(np.sum(np.power(cluster_centers[l, :] - data.iloc[j, :], 2)))
                if dist < min_dist:
                    min_dist = dist
                    min_index = l + 1
            # 标注类别
            mat[j, :] = min_dist, min_index, mat[j, 2]
        #print(mat)
        # 更新聚类中心
        new_cluster_centers = np.zeros((k, data.shape[1]))
        for j in range(k):
            # 计算新的聚类中心
            new_cluster_centers[j, :] = np.mean(data.iloc[np.nonzero(mat[:, 1].A == j + 1)[0]], axis=0)
        # cluster_centers = new_cluster_centers
        print("cluster_centers: ", cluster_centers)
        sse = cal_sse(mat, length, k)
        sse_list.append(sse)
        if np.all(cluster_centers == new_cluster_centers):
            break
        else:
            cluster_centers = new_cluster_centers
    # 计算sse
    sse = cal_sse(mat, length, k)
    # 计算准确率
    acc = gen_acc(mat, length, k)

    # 画图
    X = 6  # 总酚
    Y = 7  # 黄酮

    plt.xlabel('特征7')
    plt.ylabel('特征8')
    plt.title('SSE=%.3f Acc=%.3f' % (sse, acc))
    plt.axis([0, 1, 0, 1])
    for i in range(length):
        if int(mat[i, 1]) == 1:
            plt.scatter(data.iloc[i, X], data.iloc[i, Y], c='r', marker='o')
        elif int(mat[i, 1]) == 2:
            plt.scatter(data.iloc[i, X], data.iloc[i, Y], c='g', marker='o')
        else:
            plt.scatter(data.iloc[i, X], data.iloc[i, Y], c='b', marker='o')
    plt.savefig(os.path.join(img_dir, "res.png"))

    # 画出sse变化图
    plt.figure()
    plt.plot(range(len(sse_list)), sse_list)
    plt.xlabel('iter')
    plt.ylabel('sse')
    plt.title('SSE')
    plt.savefig(os.path.join(img_dir, "sse.png"))


