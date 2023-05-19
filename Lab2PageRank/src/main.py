import numpy as np

from config import *
from utils import *
import preprocess as pre
import pandas as pd
import os
def generate_mat()->np.array:
    df = pd.read_csv(os.path.join(data_dir, 'sent_receive.csv'))
    person = pd.read_csv(os.path.join(dataset_dir, 'Persons.csv'))

    f = open(os.path.join(data_dir, 'sent_receive.csv'))
    edges = [line.strip('\n').split(',') for line in f]
    nodes = []
    for edge in edges:
        if edge[1] not in nodes:
            nodes.append(edge[1])
        if edge[2] not in nodes:
            nodes.append(edge[2])

    # 获取人数
    num = len(nodes)
    print(num)
    # 创建邻接矩阵 mat
    mat = np.zeros((num, num))
    # 初始化M矩阵
    for edge in edges:
        start = nodes.index(edge[1])
        end = nodes.index(edge[2])
        mat[end, start] = 1
    # for index, row in df.iterrows():
    #     mat[row['sent_id'], row['receive_id']] = 1
    # 矩阵归一化
    col_sum = np.sum(mat, axis=0)
    for col in range(mat.shape[1]):
        if col_sum[col] != 0:
            mat[:, col] /= col_sum[col]
        # else :
        #     mat[:, col] = 1 / mat.shape[1]

    print("邻接矩阵为\n", mat)
    return mat

def main():
    mat = generate_mat()

    # 经典PageRank算法
    err_list1, pr1, iter_num1 = pageRank(mat=mat, n=mat.shape[0], eps=eps)

    print("经典PageRank算法：")
    print("迭代次数：", iter_num1)
    # print("PR值：", pr1)
    print("最后一次误差：", err_list1[-1])
    print("向量和", np.sum(pr1).squeeze())
    # 带有随机跳转的PageRank算法
    err_list2, pr2, iter_num2 = pageRank_teleport(mat=mat, n=mat.shape[0], eps=eps, damp=0.85)
    err_list3, pr3, iter_num3 = pageRank_teleport(mat=mat, n=mat.shape[0], eps=eps, damp=0.70)
    err_list4, pr4, iter_num4 = pageRank_teleport(mat=mat, n=mat.shape[0], eps=eps, damp=0.95)
    err_list5, pr5, iter_num5 = pageRank_teleport(mat=mat, n=mat.shape[0], eps=eps, damp=0.10)

    fig = plt.figure()
    plt.plot(err_list2, label="Lab2PageRank with teleport damp=0.85")
    plt.plot(err_list3, label="Lab2PageRank with teleport damp=0.70")
    plt.plot(err_list4, label="Lab2PageRank with teleport damp=0.95")
    # plt.plot(err_list5, label="Lab2PageRank with teleport damp=0.30")
    plt.legend()
    plt.title("Err——eps = 1e-8,damp varies")
    plt.xlabel("iter_nums")
    plt.ylabel("error_value")
    # plt.show()
    plt.savefig(os.path.join(res_dir, "Err - Iterations5.png"))

    # 输出结果
    print("引入teleport的PageRank算法：")
    print("迭代次数：", iter_num2)
    # print("PR值：", pr2)
    print("最后一次误差：", err_list2[-1])
    print("向量和", np.sum(pr1).squeeze())

    with open(os.path.join(res_dir, 'res1.txt'), 'w') as f:
        f.write("经典PageRank算法：\n")
        f.write("迭代次数：{}\n".format(iter_num1))
        f.write("最后一次误差：{}\n".format(err_list1[-1]))
        f.write("pagerank向量和:{}\n".format(np.sum(pr1).squeeze()))
        for i in range(pr1.shape[0]):
            f.write("{}, {}\n".format(i, str(pr1[i])))
        # 写入err

        f.write("\n\n\n")
        f.write("随机跳转PangRank算法：\n")
        f.write("迭代次数：{}\n".format(iter_num2))
        f.write("最后一次误差：{}\n".format(err_list2[-1]))
        f.write("向量和:{}\n".format(np.sum(pr2).squeeze()))
        for i in range(pr2.shape[0]):
            f.write("{}, {}\n".format(i+1, str(pr2[i])))

    print(err_list1)
    analyze_error(err_list1, err_list2)



if __name__ == "__main__":
    main()


