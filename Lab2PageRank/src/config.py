# -*- coding: utf-8 -*-

"""
# @File       : config.py
# @Time       : 2023/4/21
# @Author     : EightHalf
# @Version    : Python 3.11.3
# @Description: set the file path
"""
import os

# 文件目录设置
root_dir = os.path.dirname(os.path.dirname(__file__))  # 获取当前文件的上一级目录
src_dir = os.path.dirname(__file__)  # 获取当前文件的目录
dataset_dir = os.path.join(root_dir, 'datasets/datasets')  # 获取datasets目录
data_dir = os.path.join(root_dir, 'data')  # 获取data目录
res_dir = os.path.join(root_dir, 'res')  # 获取result目录

# 参数设置
eps = 1e-8  # 默认精度
damp = 0.85  # 默认阻尼系数
