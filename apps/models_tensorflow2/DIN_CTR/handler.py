#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : DIEN论文复现
# __date__: 2020/09/15 16
import csv
import io
import os
import pickle
import random
from concurrent.futures import (ALL_COMPLETED, ThreadPoolExecutor,
                                as_completed, wait)

import numpy as np
import pandas as pd
from openpyxl import Workbook

from apps.api_exception import Fail, ParameterException
from apps.constants import MAX_CPUS
from apps.data.handler import (META_ELECTRONICS, REVIEWS_ELECTRONICS_5,
                                TMP_PATH)

def build_map(df:"reviews_df / meta_df", col_name:"列名"):
    """
    制作一个映射，键为列名，值为序列数字
    :return: 字典，键
    """
    key = sorted(df[col_name].unique().tolist())
    m = dict(zip(key, range(len(key))))
    df[col_name] = df[col_name].map(lambda x: m[x])
    return m, key



def get_building_dataset(params=None):
    """
    获取处理后的测试集和训练集
    """
    if not os.path.exists(os.path.join(TMP_PATH, 'dataset.p')):
        train_set, test_set, cate_list, (user_count, item_count,
                                         cate_count, max_sl) = building_dataset(params)
    else:
        # pickle获取
        with open(os.path.join(TMP_PATH, 'dataset.p'), 'rb') as f:
            train_set = np.array(pickle.load(f),dtype=object)
            test_set = pickle.load(f)
            cate_list = pickle.load(f)
            (user_count, item_count, cate_count, max_sl) = pickle.load(f)
    return np.array(train_set,dtype=object), test_set, cate_list, (user_count, item_count, cate_count, max_sl)


def building_dataset(params=None):
    """
    获取映射后的数据，处理过用pickle缓存.
    通过获取的数据构建训练测试集：
    NOTE: 生成训练集、测试集，每个用户所有浏览的物品（共n个）前n-1个为训练集（正样本），并生成相应的负样本，每个用户共有n-2个训练集（第1个无浏览历史），第n个作为测试集。
    故测试集共有192403个，即用户的数量。训练集共2608764个
    """
    if not os.path.exists(os.path.join(TMP_PATH, 'remap.p')):
        # 处理数据
        reviews_df, cate_list, (user_count, item_count, cate_count,
                                example_count), _ = re_maping(params=None)
    else:
        # pickle获取
        with open(os.path.join(TMP_PATH, 'remap.p'), 'rb') as f:
            reviews_df = pickle.load(f)
            cate_list = pickle.load(f)
            user_count, item_count, cate_count, example_count = pickle.load(f)
    train_set, test_set = [], []
    # 最大的序列长度
    max_sl = 0
    for reviewerID, hist in reviews_df.groupby('reviewerID'):
        # 每个用户浏览过的物品，即为正样本
        pos_list = hist['asin'].tolist()
        max_sl = max(max_sl, len(pos_list))

        # 生成负样本
        def gen_neg():
            neg = pos_list[0]
            while neg in pos_list:
                neg = random.randint(0, item_count - 1)
            return neg

        # 正负样本比例1：1
        neg_list = [gen_neg() for i in range(len(pos_list))]

        for i in range(1, len(pos_list)):
            # 生成每一次的历史记录，即之前的浏览历史
            hist = pos_list[:i]
            sl = len(hist)
            if i != len(pos_list) - 1:
                # 保存正负样本，格式：用户ID，正/负物品id，浏览历史，浏览历史长度，标签（1/0）
                train_set.append((reviewerID, pos_list[i], hist, sl, 1))
                train_set.append((reviewerID, neg_list[i], hist, sl, 0))
            else:
                # 最后一次保存为测试集
                label = (pos_list[i], neg_list[i])
                test_set.append((reviewerID, hist, sl, label))

    # 打乱顺序
    random.shuffle(train_set)
    random.shuffle(test_set)

    assert len(test_set) == user_count
    # 写入dataset.pkl文件
    with open(os.path.join(TMP_PATH, 'dataset.p'), 'wb') as f:
        pickle.dump(np.array(train_set, dtype=object), f, pickle.HIGHEST_PROTOCOL)
        pickle.dump(test_set, f, pickle.HIGHEST_PROTOCOL)
        pickle.dump(cate_list, f, pickle.HIGHEST_PROTOCOL)
        pickle.dump((user_count, item_count, cate_count, max_sl),
                    f, pickle.HIGHEST_PROTOCOL)
    return np.array(train_set, dtype=object), test_set, cate_list, (user_count, item_count, cate_count, max_sl)




def re_maping(params=None):
    """
    reviews_df保留['reviewerID'【用户ID】, 'asin'【产品ID】, 'unixReviewTime'【浏览时间】]
    meta_df保留['asin'【产品ID】, 'categories'【种类】]
    """
    # reviews,meta
    pred_data = get_pred_data(params)
    reviews_df, meta_df = pred_data.get('meta'), pred_data.get('reviews')
    reviews_df = reviews_df[['reviewerID', 'asin', 'unixReviewTime']]
    meta_df = meta_df[['asin', 'categories']]

    # 类别只保留最后一个
    meta_df['categories'] = meta_df['categories'].map(lambda x: x[-1][-1])

    # meta_df文件的物品ID映射
    asin_map, asin_key = build_map(meta_df, 'asin')
    # meta_df文件物品种类映射
    cate_map, cate_key = build_map(meta_df, 'categories')
    # reviews_df文件的用户ID映射
    revi_map, revi_key = build_map(reviews_df, 'reviewerID')

    # user_count: 192403	item_count: 63001	cate_count: 801	example_count: 1689188
    user_count, item_count, cate_count, example_count = \
        len(revi_map), len(asin_map), len(cate_map), reviews_df.shape[0]
    # print('user_count: %d\titem_count: %d\tcate_count: %d\texample_count: %d' %
    #       (user_count, item_count, cate_count, example_count))

    # 按物品id排序，并重置索引
    meta_df = meta_df.sort_values('asin')
    meta_df = meta_df.reset_index(drop=True)

    # reviews_df文件物品id进行映射，并按照用户id、浏览时间进行排序，重置索引
    reviews_df['asin'] = reviews_df['asin'].map(lambda x: asin_map[x])
    reviews_df = reviews_df.sort_values(['reviewerID', 'unixReviewTime'])
    reviews_df = reviews_df.reset_index(drop=True)
    reviews_df = reviews_df[['reviewerID', 'asin', 'unixReviewTime']]

    # 各个物品对应的类别
    cate_list = np.array(meta_df['categories'], dtype='int32')

    # 保存所需数据为pkl文件
    with open(os.path.join(TMP_PATH, 'remap.p'), 'wb') as f:
        pickle.dump(reviews_df, f, pickle.HIGHEST_PROTOCOL)
        pickle.dump(cate_list, f, pickle.HIGHEST_PROTOCOL)
        pickle.dump((user_count, item_count, cate_count, example_count),
                    f, pickle.HIGHEST_PROTOCOL)
        pickle.dump((asin_key, cate_key, revi_key), f, pickle.HIGHEST_PROTOCOL)
    return reviews_df, cate_list, (user_count, item_count, cate_count, example_count), (asin_key, cate_key, revi_key)


def get_pred_data(params=None) -> dict:
    """
    预加载数据，加载完后自动存到pickle，并之后从pickle获取
    """
    params = {'meta': META_ELECTRONICS,
              'reviews': REVIEWS_ELECTRONICS_5}
    file_pathes = params.get('files')

    def json2df(file_path):
        with open(file_path, 'r') as fin:
            df = {}
            i = 0
            all_task = []
            # with ThreadPoolExecutor(MAX_CPUS) as executor:
            #     all_task += [executor.submit(ant, (df,i,line))
            #                   for line in fin]
            for line in fin:
                df[i] = eval(line)
                i += 1
            df = pd.DataFrame.from_dict(df, orient='index')
            return df

    meta_pickle = os.path.join(TMP_PATH, 'meta.p')
    reviews_pickle = os.path.join(TMP_PATH, 'reviews.p')
    if not os.path.exists(reviews_pickle):
        reviews_df = json2df(params.get('reviews'))
        with open(reviews_pickle, 'wb') as f:
            pickle.dump(reviews_df, f, pickle.HIGHEST_PROTOCOL)
    else:
        # 从缓存的文件夹获取基本被过滤后的文件
        reviews_df = pickle.load(
            open(reviews_pickle, mode='rb'))

    if not os.path.exists(meta_pickle):
        meta_df = json2df(params.get('meta'))
        meta_df = meta_df[meta_df['asin'].isin(reviews_df['asin'].unique())]
        meta_df = meta_df.reset_index(drop=True)
        with open(meta_pickle, 'wb') as f:
            pickle.dump(meta_df, f, pickle.HIGHEST_PROTOCOL)
    else:
        # 从缓存的文件夹获取基本被过滤后的文件
        meta_df = pickle.load(
            open(meta_pickle, mode='rb'))
    res = {'meta': meta_df,
              'reviews': reviews_df}
    return res


def hello_word_handler(params=None):
    res = {
        'name': 'stray_camel',
        'age': '25',
        'patient_id': '19000347',
    }
    return res

