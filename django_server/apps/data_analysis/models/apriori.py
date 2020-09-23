#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : Apriori算法实现
# __REFERENCES__ : [https://wizardforcel.gitbooks.io/dm-algo-top10/content/apriori.html, https://www.cnblogs.com/lsqin/p/9342926.html],
# __date__: 2020/09/22 09

from apps.utils.log.handler import function_logging
from numpy import *
import numpy as np
import pandas as pd
import logging
log = logging.getLogger('apps')


def loadDataSet():
    return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]

# 获取候选1项集，dataSet为事务集。返回一个list，每个元素都是set集合


@function_logging
def createC1(dataSet):
    """获取元素个数为1的项集（非频繁项集，因为还没有同最小支持度比较）"""
    # 因为除了候选1项集外其他的候选n项集都是以二维列表的形式存在，所以要将候选1项集的每一个元素都转化为一个单独的集合。
    C1 = sorted(set(item for transaction in dataSet for item in transaction))
    # map(frozenset, C1)的语义是将C1由Python列表转换为不变集合（frozenset，Python中的数据结构）
    res = list(map(frozenset, map(lambda x: [x], C1)))
    return res

# 找出候选集中的频繁项集
# dataSet为全部数据集，Ck为大小为k（包含k个元素）的候选项集，minSupport为设定的最小支持度
def scanD(dataSet, Ck, minSupport):
    """retList为在Ck中找出的频繁项集（支持度大于minSupport的），supportData记录各频繁项集的支持度"""
    ssCnt = {}   # 记录每个候选项的个数
    for tid in dataSet:
        for can in Ck:
            if can.issubset(tid):
                ssCnt[can] = ssCnt.get(can, 0) + 1   # 计算每一个项集出现的频率
    numItems = float(len(dataSet))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key] / numItems
        if support >= minSupport:
            retList.insert(0, key)  # 将频繁项集插入返回列表的首部
        supportData[''.join(map(str, key))] = support
    return retList, supportData


@function_logging
def aprioriGen(Lk, k):
    """通过频繁项集列表Lk和项集个数k生成候选项集C(k+1)。"""
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i + 1, lenLk):
            # 前k-1项相同时，才将两个集合合并，合并后才能生成k+1项
            L1 = list(Lk[i])[:k-2]
            L2 = list(Lk[j])[:k-2]   # 取出两个集合的前k-1个元素
            L1.sort()
            L2.sort()
            if L1 == L2:
                retList.append(Lk[i] | Lk[j])
    return retList


def apriori(params):
    """Apriori 算法是一种最有影响力的挖掘布尔关联规则的频繁项集的 算法,它使用一种称作逐层搜索的迭代方法，k- 项集用于探索（k+1）- 项集。首先，找出频繁 1- 项集的集合。该集合记作L1。L1 用于找频繁2- 项集的集合 L2，而L2 用于找L2，如此下去，直到不能找到 k- 项集。"""
    dataSet, minSupport, max_k = params.get(
        'data'), params.get('minSupport'), params.get('max_k')
    C1 = createC1(dataSet)  # 从事务集中获取候选1项集
    D = list(map(set, dataSet))  # 将事务集的每个元素转化为集合
    L1, supportData = scanD(D, C1, minSupport)   # 获取频繁1项集和对应的支持度
    L = [L1]  # L用来存储所有的频繁项集
    k = max_k
    while (len(L[k-max_k]) > 0):  # 一直迭代到项集数目过大而在事务集中不存在这种n项集
        Ck = aprioriGen(L[k-max_k], k)   # 根据频繁项集生成新的候选项集。Ck表示项数为k的候选项集
        Lk, supK = scanD(D, Ck, minSupport)  # Lk表示项数为k的频繁项集，supK为其支持度
        L.append(Lk)
        supportData.update(supK)  # 添加新频繁项集和他们的支持度
        k += 1

    # 将L中的frozenset转化为字符串
    def _(x): return ''.join(map(str, x))
    res_data = [sorted(map(_, i)) for i in L if i]
    res = {'origin_data': dataSet, 'supportData': supportData,
           'description': apriori.__doc__, 'res_data': res_data, 'minSupport': minSupport, 'max_(k)items':max_k}
    return res

if __name__ == "__main__":
    data = loadDataSet()