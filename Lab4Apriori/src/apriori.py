from utils import *
import time


# 生成候选频繁一项集
@timer
def generate_c1(data_set: list[list]) -> set:
    """生成候选频繁一项集
    :param data_set: 数据集
    :return: 候选频繁一项集
    """
    c1 = set()
    for basket in data_set:
        for item in basket:
            # frozenset:冻结集合，可以作为字典的key
            item = frozenset([item])
            c1.add(item)
        
    return c1


@timer
def generate_lk(data_set: list[list], ck: set[frozenset], min_support: float = MIN_SUPPORT_OF_FREQ_ITEMS) \
        -> tuple[set[frozenset], dict[frozenset, float]]:
    """
    根据 Ck 生成频繁 k 项集 Lk
    :param data_set: 数据集
    :param ck: 候选频繁项集
    :param min_support: 最小支持度
    :return: 频繁 k 项集 Lk, 频繁项集支持度
    """
    # 字典，记录每个候选频繁项集出现的次数
    item_set_count = {}
    # 频繁k项集
    lk = set()
    # 记录频繁项集的支持度
    fre_item_set_sup = {}
    for basket in data_set:
        for item_set in ck:
            if item_set.issubset(basket):
                # 统计候选频繁项集出现次数
                if item_set in item_set_count:
                    item_set_count[item_set] += 1
                else:
                    item_set_count[item_set] = 1
    data_num = len(data_set)
    for key, value in item_set_count.items():
        # 计算支持度
        support = value / data_num
        if support >= min_support:
            lk.add(key)
            fre_item_set_sup[key] = support
    return lk, fre_item_set_sup


def is_k_sub(k_item_set: frozenset, lk: set) -> bool:
    """
    判断 k 项集是否是 k + 1 项子集
    :param k_item_set: k 项集
    :param lk: k 阶频繁项集
    :return: k 项集是否是 k + 1 项子集
    """
    for item in k_item_set:
        sub_item = k_item_set - frozenset([item])
        if sub_item not in lk:
            return False
    return True


@timer
def generate_next_ck(lk: set[frozenset], k: int) -> set[frozenset]:
    """
    根据 Lk 构造候选频繁项集 Ck+1
    :param lk: 频繁项集 Lk
    :param k: 频繁项集基数
    :return: 频繁候选项集 Ck+1
    """
    ck = set()
    for set1 in lk:
        for set2 in lk:
            union_set = set1 | set2
            # * 剪枝策略和连接策略
            if len(union_set) == k and is_k_sub(union_set, lk):
                ck.add(union_set)
    return ck


# 生成符合置信度要求的关联规则
@timer
def generate_rules(l3: set[frozenset], sup1: dict[frozenset, float], sup2: dict[frozenset, float],
                   sup3: dict[frozenset, float], min_confidence: float = MIN_CONFIDENCE):
    """
    生成符合置信度要求的关联规则
    :param l3: 三阶频繁项集
    :param sup1: 一阶频繁项集支持度
    :param sup2: 二阶频繁项集支持度
    :param sup3: 三阶频繁项集支持度
    :param min_confidence: 最小置信度要求
    :return: 关联规则列表
    """
    rule_list = []
    for fre_item_set in l3:
        union_sup = sup3[fre_item_set]
        for k in range(3):
            tmp = list(fre_item_set)
            set1 = [tmp[k]]
            tmp.remove(tmp[k])
            set2 = tmp
            conf12 = union_sup / sup1[frozenset(set1)]
            conf21 = union_sup / sup2[frozenset(set2)]
            if conf12 >= min_confidence:
                rule_list.append((set(set1), set(set2), conf12))
            if conf21 >= min_confidence:
                rule_list.append((set(set2), set(set1), conf21))
    return rule_list


def save_fre_item_set(filename: str, fre_item_set_sup: dict[frozenset, float]) -> None:
    """保存频繁项集
    :param filename: 文件名
    :param fre_item_set_sup: 频繁项集支持度
    """
    f_write = open(os.path.join(res_dir, filename), 'w')
    f_write.write('[],\t[]\n'.format('frequent-itemSets', 'support'))
    for k, v in fre_item_set_sup.items():
        f_write.write("[],\t[]\n".format(set(k), v))
    # f_write.write("total: {}".format(len(fre_item_set_sup)))
    print("{} done.".format(filename))


def save_rules(filename: str, rule_list: list) -> None:
    """保存关联规则
    :param filename: 文件名
    :param rule_list: 关联规则
    """
    f_write = open(os.path.join(res_dir, filename), 'w')
    for rule in rule_list:
        f_write.write("[] => [], []\n".format(rule[0], rule[1], rule[2]))

