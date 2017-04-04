import pandas as pd
import numpy as np
from sklearn import cross_validation as cv
import urllib


N = 10
def read_file(name):
    user_dict = dict()
    item_ditc = dict()
    header = ['user_id', 'item_id', 'rating', 'timestamp']
    df = pd.read_csv(name, sep='\t', names=header)
    train, test = cv.train_test_split(df, test_size=0.25)
    for line in train.itertuples():
        user_dict.setdefault(line[1], []).append([line[2], int(line[3])])
        item_ditc.setdefault(line[2], []).append([line[1], int(line[3])])
    test = dict()
    for line in train.itertuples():
        test.setdefault(line[1], []).append(line[2])
    # with open(name) as f:
    #     for line in f.readlines():
    #         datas = line.split('\t')
    #         user_dict.setdefault(datas[0], []).append([datas[1], int(datas[2])])
    #         item_ditc.setdefault(datas[1], []).append([datas[0], int(datas[2])])
    print test
    return user_dict, item_ditc, test

def read_user(name):
    user_map = dict()
    with open(name) as f:
        for line in f.readlines():
            user = line.split('|')
            user_map[user[0]] = [user[1], user[2], user[3]]
    return user_map

def read_item(name):
    item_map = dict()
    with open(name) as f:
        for line in f.readlines():
            item = line.split('|')
            item_map[item[0]] = [item[1], item[2], item[3], item[4]]
    return item_map

def precision(user_dict, test_data, sim, user_id, k):
    all = 0
    hit = 0
    for user in user_dict.keys():
        tu = test_data[user]
        rank = recommend(user, sim, user_dict, k)
        for item, rank_val in rank:
            if item in tu:
                hit += 1
        all += N
    print 'pre', hit, all
    return hit*1.0/all

def user_sim_cos(user_dict, item_dict):
    simi = dict()
    rec = dict()
    norm = dict()
    for item, user_rate in item_dict.items():
        for u, u_rate in user_rate:
            norm[u] = norm.setdefault(u, 0) + 1 # pow(u_rate, 2)
            for v, v_rate in user_rate:
                if u != v:
                    rec.setdefault(u, dict()).setdefault(v, 0)
                    rec[u][v] += 1 # u_rate * v_rate # 1/np.log(1+len(user_rate))
    for u, v_dict in rec.items():
        simi.setdefault(u, dict())
        for v, res in v_dict.items():
            simi[u][v] = res/np.sqrt(float(norm[u]*norm[v]))
    return simi

def recommend(user, sim, user_dict, k):
    rank = dict()
    stop_item = [x for x, y in user_dict[user]]
    for v, wuv in sorted(sim[user].items(), key=lambda x:x[1], reverse=True)[:k]:
        for item, rate in user_dict[v]:
            if item not in stop_item:
                rank[item] = rank.setdefault(item, 0) + wuv * rate
    return list(sorted(rank.items(), key=lambda x: x[1], reverse=True))

if __name__ == '__main__':
    user_dict, item_ditc, test = read_file('../data/ml-100k/u.data')
    sim = user_sim_cos(user_dict, item_ditc)
    rank = recommend(447, sim, user_dict, 3)

    user_map = read_user('../data/ml-100k/u.user')
    item_map = read_user('../data/ml-100k/u.item')

    for item_id, pui in rank[:10]:
        print 'movie: ', item_map[str(item_id)][0], 'rank: ', pui

    print rank
    print test[447]
    hit = 0
    for x, y in rank:
        if x in test[447]:
            hit += 1
    print 'hit', hit

    # pre = precision(user_dict, test, sim, '447', 3)
    # print 'precision: ', pre

