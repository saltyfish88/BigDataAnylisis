import os
from config import *
def timer(func):
    """
    计时器装饰器
    :param func:
    :return:
    """

    def func_wrapper(*args, **kwargs):
        from time import time
        time_start = time()
        result = func(*args, **kwargs)
        time_end = time()
        time_spend = time_end - time_start
        print('%s cost time: %.3f s' % (func.__name__, time_spend))
        return result

    return func_wrapper

def get_datafile(filename: str) -> str:
    """获取完整文件名

    Args:
        filename (str): 文件名

    Returns:
        str: 包含完整路径的文件名
    """
    return os.path.join(data_dir, filename)


