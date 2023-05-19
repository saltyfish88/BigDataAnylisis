# -*- coding: utf-8 -*-

"""
# @File       : config.py
# @Time       : 2023/4/28
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

# 参数设置
MIN_SUPPORT_OF_FREQ_ITEMS = 0.005  # 频繁项集最小支持度
MIN_CONFIDENCE = 0.5  # 关联规则最小置信度
MIN_LIFT = 1.0  # 关联规则最小提升度
max_hash_size = 1000