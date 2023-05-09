# -*- coding: utf-8 -*-

"""
# @File       : config.py
# @Time       : 2023/4/14
# @Author     : EightHalf
# @Version    : Python 3.11.3
# @Description: set the file path
"""
import os

# 文件目录设置
root_dir = os.path.dirname(os.path.dirname(__file__))  # 获取当前文件的上一级目录
src_dir = os.path.dirname(__file__)  # 获取当前文件的目录
data_dir = os.path.join(root_dir, 'data')  # 获取data目录
res_dir = os.path.join(root_dir, 'res')  # 获取result目录

# Map-Reduce参数设置
Map_Node_Num = 9  # Map节点个数
Combine_Node_Num = 9  # Combine节点个数
Shuffle_Node_Num = 3  # Shuffle节点个数
Reduce_Node_Num = 3  # Reduce节点个数

