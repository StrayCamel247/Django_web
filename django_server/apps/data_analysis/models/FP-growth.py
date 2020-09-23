#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : FP树生成频繁项集
# __REFERENCES__ : [https://www.cnblogs.com/lsqin/p/9342926.html]
# __date__: 2020/09/22 10
from apps.utils.log.handler import function_logging


def loadSimpDat():
    """生成数据集"""
    simpDat = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    return simpDat


def createInitSet(dataSet):
    """将数据集转化为目标格式"""
    retDict = {frozenset(trans): 1 for trans in dataSet}
    return retDict


class treeNode:
    def __init__(self, nameValue, count, parentNode):
        self.name = nameValue
        # 出现次数
        self.count = count
        self.next = None
        # 指向父节点的指针
        self.parent = parentNode
        self.childrens = {}  # 指向子节点的字典，以子节点的元素名称为键，指向子节点的指针为值，初始化为空字典

    def count_add(self, count):
        self.count += count

    def __str__(self, ind=1):
        for child in self.childrens.values():
            print(child.__str__(ind + 1))
        return '第{n}层：，name为：{name}，出现{count}次'.format(n=ind, name=self.name, count=self.count)


def updateHeader(nodeToTest, targetNode):
    while (nodeToTest.next != None):
        nodeToTest = nodeToTest.next
    nodeToTest.next = targetNode


def updateTree(items, inTree, headerTable, count):
    """根据一个排序过滤后的频繁项更新FP树"""
    if items[0] in inTree.childrens:
        inTree.childrens[items[0]].count_add(count)
    else:
        # 没有这个元素项时创建一个新节点
        inTree.childrens[items[0]] = treeNode(items[0], count, inTree)
        # 更新头指针表或前一个相似元素项节点的指针指向新节点
        if headerTable[items[0]][1] == None:  # 如果是第一次出现，则在头指针表中增加对该节点的指向
            headerTable[items[0]][1] = inTree.childrens[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.childrens[items[0]])

    if len(items) > 1:
        # 对剩下的元素项迭代调用updateTree函数
        updateTree(items[1::], inTree.childrens[items[0]], headerTable, count)


def createTree(dataSet, minSpport=1):
    """创建FP树。dataSet为事务集，为一个字典，键为每个事物，值为该事物出现的次数。minSup为最低支持度"""
    # 第一次遍历数据集，创建头指针表
    headerTable = {}
    for trans in dataSet:
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
    # 移除不满足最小支持度的元素项
    headerTable = dict(
        filter(lambda i: i[1] >= minSpport, headerTable.items()))
    # 空元素集，返回空
    if not headerTable:
        return None, None
    retTree = treeNode('root node', None, None)  # 根节点
    # 增加一个数据项，用于存放指向相似元素项指针
    for k in headerTable:
        headerTable[k] = [headerTable[k], None]
    # 第二次遍历数据集，创建FP树
    for tranSet, count in dataSet.items():
        localD = {}  # 记录频繁1项集的全局频率，用于排序
        for item in tranSet:
            if item in headerTable:
                localD[item] = headerTable[item][0]
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(
                localD.items(), key=lambda p: p[1], reverse=True)]
            updateTree(orderedItems, retTree, headerTable, count)  # 更新FP树
    return retTree, headerTable


def ascendTree(leafNode, prefixPath):
    """查找元素条件模式基: 直接修改prefixPath的值，将当前节点leafNode添加到prefixPath的末尾，然后递归添,prefixPath就是一条从treeNode（包括treeNode）到根节点（不包括根节点）的路径加其父节点。"""
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)


def findPrefixPath(basePat, treeNode):
    """为给定元素项生成一个条件模式基（前缀路径）。basePet表示输入的频繁项，treeNode为当前FP树中对应的第一个节点,函数返回值即为条件模式基condPats，用一个字典表示，键为前缀路径，值为计数值。"""
    condPats = {}  # 存储条件模式基
    while treeNode != None:
        prefixPath = []  # 用于存储前缀路径
        ascendTree(treeNode, prefixPath)  # 生成前缀路径
        if len(prefixPath) > 1:
            # 出现的数量就是当前叶子节点的数量
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        # 遍历下一个相同元素
        treeNode = treeNode.next
    return condPats


def mineTree(inTree, headerTable, minSpport: "最小支持度", preFix: "在函数中用于保存当前前缀" = set(), freqItemList: "用来储存生成的频繁项集" = []):
    # 对频繁项按出现的数量进行排序进行排序
    # 返回重新排序的列表。每个元素是一个元组，[（key,[num,treeNode],()）
    sorted_headerTable = sorted(headerTable.items(), key=lambda p: p[1][0])
    # 获取频繁项
    bigL = [v[0] for v in sorted_headerTable]

    for basePat in bigL:
        newFreqSet = preFix.copy()  # 新的频繁项集
        newFreqSet.add(basePat)     # 当前前缀添加一个新元素
        freqItemList.append(newFreqSet)  # 所有的频繁项集列表
        # 获取条件模式基。就是basePat元素的所有前缀路径。它像一个新的事务集
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        myCondTree, myHead = createTree(condPattBases, minSpport)  # 创建条件FP树
        if myHead != None:
            # 用于测试
            print('conditional tree for:', newFreqSet)
            print(myCondTree)
            # 递归查找频繁项集
            mineTree(myCondTree, myHead, minSpport,
                     newFreqSet, freqItemList)


@function_logging
def ft_growth(params):
    """在关联分析中，频繁项集的挖掘最常用到的就是Apriori算法。Apriori算法是一种先产生候选项集再检验是否频繁的“产生-测试”的方法。这种方法有种弊端：当数据集很大的时候，需要不断扫描数据集造成运行效率很低。而FP-Growth算法就很好地解决了这个问题。它的思路是把数据集中的事务映射到一棵FP-Tree上面，再根据这棵树找出频繁项集。FP-Tree的构建过程只需要扫描两次数据集。

    根据事务集获取FP树和频繁项。
    遍历频繁项，生成每个频繁项的条件FP树和条件FP树的频繁项
    这样每个频繁项与他条件FP树的频繁项都构成了频繁项集"""
    minSpport = 3
    simpDat = loadSimpDat()  # 加载数据集
    initSet = createInitSet(simpDat)  # 转化为符合格式的事务集
    myFPtree, myHeaderTab = createTree(initSet, minSpport)  # 形成FP树
    # myFPtree.__str__()  # 打印树
    freqItems = []  # 用于存储频繁项集
    # trees = 'input':{
    mineTree(myFPtree, myHeaderTab, minSpport, set([]), freqItems)  # 获取频繁项集
    res = {'data': simpDat, 'minSpport': minSpport,
           'description': ft_growth.__doc__, 'freqItems': freqItems}
    return res


if __name__ == '__main__':
    pass
