from config import *
import pandas as pd


def get_data(filename: str) -> pd.DataFrame:
    """
    读取数据
    :param filename: 文件名
    :return: 数据, DataFrame
    """
    data = pd.read_csv(os.path.join(DATA_DIR, filename))
    return data


def generate_utility_mat() -> pd.DataFrame:
    """
    Generate utility matrix from the train set
    :return: utility matrix
    """
    # Generate utility matrix
    # utility mat
    train_file = open(os.path.join(DATA_DIR, 'train_set.csv'), 'r', encoding='utf-8')
    # * train_file: 存放每位用户评论的电影和评分
    # * train_file 是一个嵌套字典
    train_data = {}
    for line in train_file.readlines()[1:]:
        line = line.strip().split(',')
        # line[0] 为用户 id，line[1] 为电影 id，line[2] 为评分
        if line[0] not in train_data.keys():
            train_data[line[0]] = {line[1]: line[2]}
        else:
            train_data[line[0]][line[1]] = line[2]
    # * 效用矩阵
    utility_mat = pd.DataFrame(train_data).fillna(0).astype(float)
    return utility_mat
