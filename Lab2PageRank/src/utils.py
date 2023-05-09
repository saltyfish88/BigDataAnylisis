import numpy as np
import matplotlib.pyplot as plt
import os
from config import *

def pageRank(mat:np.array, n, eps):
    """
    :param mat: 邻接矩阵
    :param n: 矩阵的维度
    :param eps: 精度
    :return: 返回误差列表，PR值，迭代次数
    """
    # 初始化PR值
    pr = np.ones(n) / n
    # 迭代次数
    iter_num = 0
    # 误差列表
    err_list = []
    # 迭代计算
    while True:
        # 迭代次数加1
        iter_num += 1
        # 计算PR值
        pr_ = np.dot(mat, pr)
        pr_ /= np.sum(pr_)
        # 计算误差 公式为：sqrt(sum((pr_-pr)^2))
        err = np.sqrt(np.sum(np.square(pr_ - pr)))
        # 更新PR值
        pr = pr_
        # 保存误差
        err_list.append(err)
        # 判断是否达到精度
        if err < eps:
            break
    return err_list, pr, iter_num

def pageRank_teleport(mat, n, eps, damp):
    """
    :param mat: 邻接矩阵
    :param n: 矩阵的维度
    :param eps: 精度
    :param damp: 阻尼系数
    :return: 返回误差列表，PR值，迭代次数
    """
    # 初始化PR值
    pr = np.ones(n) / n
    # 迭代次数
    iter_num = 0
    # 误差列表
    err_list = []
    # 根据阻尼系数计算矩阵
    mat_ = damp * mat + (1 - damp) / n * np.ones((n, n))
    # 迭代计算
    while True:
        # 迭代次数加1
        iter_num += 1

        # 计算PR值 公式为：PR=αM*PR+(1-α)*e/n
        pr_ = np.dot(mat_, pr)  # 矩阵相乘
        # 归一化
        pr_ /= np.sum(pr_)
        # 计算误差
        err = np.sqrt(np.sum(np.square(pr_ - pr)))
        # 保存误差
        err_list.append(err)
        # 判断是否达到精度
        if err < eps:
            break
        # 更新PR值
        pr = pr_
    return err_list, pr, iter_num



def analyze_error(err1, err2):
    """
    :param err1:
    :param err2:
    :return:
    """
    fig = plt.figure()
    plt.plot(err1, label="Lab2PageRank")
    plt.plot(err2, label="Lab2PageRank with teleport beta=0.85")
    plt.legend()
    plt.title("Err - Iterations")
    plt.xlabel("iter")
    plt.ylabel("error")
    plt.show()
    plt.savefig(os.path.join(res_dir, "Err - Iterations1.png"))

