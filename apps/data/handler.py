#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : 模型运行等数据集存储地方
# __date__: 2020/09/21 15
from django.db.models import constraints
from pyspark import SparkContext, SparkConf
import logging
import pandas as pd
import numpy as np
import os
current_floder = os.path.dirname(__file__)
# (模型) 媒体存放文件夹
MEDIA_PATH = os.path.join(os.path.dirname(
    os.path.dirname(current_floder)), 'media/models/')
# 模型日志文件夹
MODELSLOG_PATH = os.path.join(current_floder, 'models_logs')
# tensorflow checkpoint 文件夹
CHECKPOINT_PATH = os.path.join(current_floder, 'checkpoint')
# 缓存数据目录
TMP_PATH = os.path.join(current_floder, 'tmp')
# ml电影的评分数据集
ML_1M_RATINGS_FILE = os.path.join(current_floder, 'ml-1m\\ratings.csv')
# 图书据数据目录
BX_CSV_DUMP_FLODER = os.path.join(current_floder, 'BX-CSV-Dump')
# amazon数据集目录
META_ELECTRONICS = os.path.join(
    current_floder, 'Amazon\\meta_Electronics.json')
REVIEWS_ELECTRONICS_5 = os.path.join(
    current_floder, 'Amazon\\reviews_Electronics_5.json')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def get_iris_data(*args, **kwargs):
    """通过sklearn获取iris数据集"""
    from sklearn.datasets import load_iris
    iris_data = load_iris()
    per_page = kwargs.get('per_page', 10)
    page = kwargs.get('page',1)
    # label_name-
    data = np.column_stack((iris_data.data, iris_data.target))
    paginator = Paginator(data, per_page)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    title_columns = iris_data.feature_names+['label']
    all_pages = contacts.paginator.num_pages
    data_length = contacts.paginator.count
    res = {
        'max_pages_num':all_pages,
        'data_length':data_length,
        'per_page':per_page,
        'page':page,
        'data':contacts.object_list.tolist(),
        'title':title_columns
    }
    return res


def get_ml_1m_ratings_df():
    ratings_df = pd.read_csv(ML_1M_RATINGS_FILE, sep=',', engine='python')
    return ratings_df
