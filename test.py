#coding:utf-8

import numpy as np
import pandas as pd
import time
from sklearn import cross_validation as cv
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.metrics import mean_squared_error
from math import sqrt

def read_file():

    header = ['user_id', 'item_id', 'rating', 'timestamp']
    df = pd.read_csv("data/ml-100k/u.data",sep = '\t',names = header)
    #去重之后得到一个元祖，分别表示行与列,大小分别为943与1682
    n_users = df.user_id.unique().shape[0]
    n_items = df.item_id.unique().shape[0]

    print 'all users is :' + str(n_users) + ', all items is :' + str(n_items)

    #将样本分为训练集与测试机
    train_data,test_data = cv.train_test_split(df,test_size = 0.25)

    train_data_matrix = np.zeros((n_users,n_items))
    for line in train_data.itertuples():
        train_data_matrix[line[1]-1, line[2]-1] = line[3]

    test_data_matrix = np.zeros((n_users,n_items))
    for line in test_data.itertuples():
        test_data_matrix[line[1]-1,line[2]-1] = line[3]

    #计算user相似矩阵与item相似矩阵,大小分别为943*943,1682*1682
    user_similar = pairwise_distances(train_data_matrix, metric = "cosine")
    item_similar = pairwise_distances(train_data_matrix.T, metric = "cosine")

    return (train_data_matrix,test_data_matrix,user_similar,item_similar)

train_data_matrix,test_data_matrix,user_similar,item_similar = read_file()
print 'user_similar.shape is :',user_similar.shape
print 'item_similar.shape is :',item_similar.shape

def predict(rating, similar, type = 'user'):
    if type == 'user':
        mean_user_rating = rating.mean(axis = 1)
        rating_diff = (rating - mean_user_rating[:,np.newaxis])
        pred = mean_user_rating[:,np.newaxis] + similar.dot(rating_diff) / np.array([np.abs(similar).sum(axis=1)]).T
    elif type == 'item':
        pred = rating.dot(similar) / np.array([np.abs(similar).sum(axis=1)])

    return pred

user_prediction = predict(train_data_matrix, user_similar, type = 'user')
item_prediction = predict(train_data_matrix, item_similar, type = 'item')

def rmse(prediction,ground_truth):
    prediction = prediction[ground_truth.nonzero()].flatten()
    ground_truth = ground_truth[ground_truth.nonzero()].flatten()
    return sqrt(mean_squared_error(prediction, ground_truth))

print 'User based CF RMSE: ' + str(rmse(user_prediction, test_data_matrix))
print 'Item based CF RMSe: ' + str(rmse(item_prediction, test_data_matrix))