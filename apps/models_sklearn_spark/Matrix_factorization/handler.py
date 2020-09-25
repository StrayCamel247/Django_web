#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : 矩阵分解
# __date__: 2020/09/09 09

try:
    from apps.data.handler import get_ml_1m_ratings_df
except:
    pass
from math import sqrt
from sklearn.metrics import mean_squared_error
from scipy.sparse.linalg import svds
from sklearn.model_selection import cross_validate, train_test_split
import sys
import os
import numpy as np
import pandas as pd
from functools import lru_cache
# sys.path.append(os.path.dirname(os.path.abspath('./')))
# from apps.models_sklearn_spark.Matrix_factorization.handler import ratings_df
# apps_floder = os.path.dirname(os.path.dirname(__file__))
# ratings_file = os.path.join(apps_floder, 'data\\ml-1m\\ratings.csv')
# ratings_df = pd.read_csv(ratings_file, sep=',', engine='python')


def data_split(
        ratings_df: '数据',
        ratio: '分割数据的比例' = 1/4) -> (pd.DataFrame, pd.DataFrame):
    """
    按照ratio比例分割数据
    """
    train_data = ratings_df.head(round(len(ratings_df)*ratio))
    test_data = ratings_df.tail(round(len(ratings_df)*(1-ratio)))
    return train_data, test_data


def get_data_sparsity(ratings_df, n_users, n_movies) -> float:
    """
    计算数据集的稀疏度
    """
    sparsity = round(ratings_df.size/float(n_users*n_movies), 3)
    print('The sparsity level of MovieLens is ' + str(sparsity))
    return sparsity


def create_uesr_item(ratings_df, n_users, n_movies) -> (np.ndarray, np.ndarray):
    """
    创建uesr-item矩阵，此处需创建训练和测试两个UI矩阵,n_users cols * n_movies rows
    """
    train_data, test_data = data_split(ratings_df)

    train_data_matrix = np.zeros((n_users, n_movies))
    for line in train_data.itertuples():
        train_data_matrix[line[1] - 1, line[2] - 1] = line[3]

    test_data_matrix = np.zeros((n_users, n_movies))
    for line in test_data.itertuples():
        test_data_matrix[line[1] - 1, line[2] - 1] = line[3]
    return train_data_matrix, test_data_matrix


def rmse(prediction, ground_truth) -> float:
    prediction = prediction[ground_truth.nonzero()].flatten()
    ground_truth = ground_truth[ground_truth.nonzero()].flatten()
    res = sqrt(mean_squared_error(prediction, ground_truth))
    return res


@lru_cache(None)
def mf_svds(k) -> (float, np.ndarray):
    ratings_df = get_ml_1m_ratings_df()
    n_users = max(ratings_df.UserID.unique())
    n_movies = max(ratings_df.MovieID.unique())
    print('Number of users = ' + str(n_users) +
          ' | Number of movies = ' + str(n_movies))

    train_data_matrix, test_data_matrix = create_uesr_item(
        ratings_df, n_users, n_movies)

    u, s, vt = svds(train_data_matrix, k=20)
    u.shape, s.shape, vt.shape
    s_diag_matrix = np.diag(s)
    X_pred = np.dot(np.dot(u, s_diag_matrix), vt)
    _rmse = rmse(X_pred, test_data_matrix)
    print('User-based CF MSE: ' + str(_rmse))
    return _rmse, X_pred
