# -*- coding: utf-8 -*-

"""
# @File       : init.py
# @Time       : 2022/5/3
# @Author     : EightHalf
# @Version    : Python 3.11
# @Description: 初始化文件，用于设置文件目录
"""

import os

# 文件目录
# 项目根目录
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 数据目录
DATA_DIR = os.path.join(ROOT_DIR, 'data')
# 代码目录
SRC_DIR = os.path.join(ROOT_DIR, 'src')
# 结果目录
RESULT_DIR = os.path.join(ROOT_DIR, 'res')
# 图片目录
IMG_DIR = os.path.join(ROOT_DIR, 'image')

# 参数设置
# 相似用户数
K = 100
# 推荐电影数
N = 10
# hash函数个数
NUM_HASH_FUNCS = 100