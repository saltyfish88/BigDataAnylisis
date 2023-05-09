import threading
import os
import config


def create_thread(target, idx, src_str, dis_str) -> threading.Thread:
    """
    :param target: the function to be executed in the thread
    :param idx: the threadc idx
    :param src_str:
    :param dis_str:
    :return:
    """
    src_path = os.path.join(config.data_dir, src_str + str(idx))
    if(dis_str == "shuffle"):
        dis_path = os.path.join(config.data_dir, dis_str)
    else:
        dis_path = os.path.join(config.data_dir, dis_str + str(idx))
    thread = threading.Thread(target=target(src_path,dis_path), args=(src_path, dis_path))
    return thread
