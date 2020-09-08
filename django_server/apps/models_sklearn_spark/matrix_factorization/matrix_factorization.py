#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __date__: 2020/09/08 16

from math import sqrt
from sklearn.metrics import mean_squared_error
from scipy.sparse.linalg import svds
from sklearn.model_selection import cross_validate, train_test_split
import sys
import os
import numpy as np
import pandas as pd
from functools import lru_cache
apps_floder = os.path.dirname(os.path.dirname(__file__))
ratings_file = os.path.join(apps_floder, 'data\\ml-1m\\ratings.csv')
ratings_df = pd.read_csv(ratings_file, sep=',', engine='python')

n_users = max(ratings_df.UserID.unique())
n_movies = max(ratings_df.MovieID.unique())
print('Number of users = ' + str(n_users) +' | Number of movies = ' + str(n_movies))
      
# 按照1：3的比例分割数据
train_data = ratings_df.head(round(len(ratings_df)*0.25))
test_data = ratings_df.tail(round(len(ratings_df)*0.75))

# 计算数据集的稀疏度
sparsity = round(ratings_df.size/float(n_users*n_movies), 3)
print('The sparsity level of MovieLens is ' + str(sparsity))

# 创建uesr-item矩阵，此处需创建训练和测试两个UI矩阵,6040 cols * 3952 rows
train_data_matrix = np.zeros((n_users, n_movies))
for line in train_data.itertuples():
    train_data_matrix[line[1] - 1, line[2] - 1] = line[3]

test_data_matrix = np.zeros((n_users, n_movies))
for line in test_data.itertuples():
    test_data_matrix[line[1] - 1, line[2] - 1] = line[3]
    
def rmse(prediction, ground_truth):
    prediction = prediction[ground_truth.nonzero()].flatten()
    ground_truth = ground_truth[ground_truth.nonzero()].flatten()
    return sqrt(mean_squared_error(prediction, ground_truth))
    
@lru_cache(None)
def mf_svds(k):
    u, s, vt = svds(train_data_matrix, k=20)
    u.shape, s.shape, vt.shape
    s_diag_matrix = np.diag(s)
    X_pred = np.dot(np.dot(u, s_diag_matrix), vt)
    print('User-based CF MSE: ' + str(rmse(X_pred, test_data_matrix)))
    return rmse(X_pred, test_data_matrix)

if __name__ == "__main__":
    print(mf_svds(20))