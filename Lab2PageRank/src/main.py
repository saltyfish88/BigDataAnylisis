import numpy as np

from config import *
from utils import *
import Lab2PageRank.src.preprocess as pre
import pandas as pd
import os
def generate_mat()->np.array:
    df = pd.read_csv(os.path.join(data_dir, 'sent_receive.csv'))
    person = pd.read_csv(os.path.join(dataset_dir, 'Persons.csv'))
    num = person.shape[0]
    # 创建矩阵 mat
    mat = np.zeros((num, num))

    for index, row in df.iterrows():
        mat[row['sent_id'], row['receive_id']] += 1

    # * 矩阵归一化
    col_sum = np.sum(mat, axis=0)
    for col in range(mat.shape[1]):
        if col_sum[col] != 0:
            mat[:, col] /= col_sum[col]

    print("邻接矩阵为\n", mat)
    return mat

def main():
    mat = generate_mat()

    # 经典PageRank算法
    err_list1, pr1, iter_num1 = pageRank(mat=mat, n=mat.shape[0], eps=eps)

    print("经典PageRank算法：")
    print("迭代次数：", iter_num1)
    print("PR值：", pr1)
    print("最后一次误差：", err_list1[-1])
    print("向量和", np.sum(pr1).squeeze())
    # 带有随机跳转的PageRank算法
    err_list2, pr2, iter_num2 = pageRank_teleport(mat=mat, n=mat.shape[0], eps=eps, damp=damp)


    # 输出结果
    print("带有随机跳转的PageRank算法：")
    print("迭代次数：", iter_num2)
    print("PR值：", pr2)
    print("最后一次误差：", err_list2[-1])
    print("向量和", np.sum(pr1).squeeze())

    with open(os.path.join(res_dir, 'res1.txt'), 'w') as f:
        f.write("经典PageRank算法：\n")
        f.write("迭代次数：{}\n".format(iter_num1))
        f.write("最后一次误差：{}\n".format(err_list1[-1]))
        f.write("向量和:{}\n".format(np.sum(pr1).squeeze()))
        for i in range(pr1.shape[0]):
            f.write("{}, {}\n".format(i, str(pr1[i])))

        f.write("\n\n\n")
        f.write("随机跳转PangRank算法：\n")
        f.write("迭代次数：{}\n".format(iter_num2))
        f.write("最后一次误差：{}\n".format(err_list2[-1]))
        f.write("向量和:{}\n".format(np.sum(pr2).squeeze()))
        for i in range(pr2.shape[0]):
            f.write("{}, {}\n".format(i+1, str(pr2[i])))


    analyze_error(err_list1, err_list2)



if __name__ == "__main__":
    main()


