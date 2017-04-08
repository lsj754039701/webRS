# -*- coding=utf-8 -*-
import pandas as pd
import numpy as np
from sklearn import cross_validation as cv


class CF:
    def __init__(self, k, type='user'):
        self.simi = dict()
        self.N = 10
        self.user_item = dict()
        self.item_user = dict()
        self.test = dict()
        self.k = k
        self.user_map = self.read_user('../data/ml-100k/u.user')
        self.item_map = self.read_item('../data/ml-100k/u.item')
        self.type = type

    def read_file(self, name):
        header = ['user_id', 'item_id', 'rating', 'timestamp']
        df = pd.read_csv(name, sep='\t', names=header)
        train, test = cv.train_test_split(df, test_size=0.3)
        for line in train.itertuples():
            self.user_item.setdefault(line[1], []).append([line[2], int(line[3])])
            self.item_user.setdefault(line[2], []).append([line[1], int(line[3])])
        for line in test.itertuples():
            self.test.setdefault(line[1], []).append(line[2])

    def read_user(self, name):
        user_map = dict()
        with open(name) as f:
            for line in f.readlines():
                user = line.split('|')
                user_map[user[0]] = [user[1], user[2], user[3]]
        return user_map

    def read_item(self, name):
        item_map = dict()
        with open(name) as f:
            for line in f.readlines():
                item = line.split('|')
                item_map[item[0]] = [item[1], item[2], item[3], item[4]]
        return item_map

    def calc_simi_cos(self, train):
        norm = dict()
        rec = dict()
        for id, id_rate in train.items():
            for i, i_rate in id_rate:
                norm[i] = norm.setdefault(i, 0) + pow(i_rate, 2)
                for j, j_rate in id_rate:
                    rec.setdefault(i, dict()).setdefault(j, 0)
                    rec[i][j] += i_rate * j_rate
        for i, j_dict in rec.items():
            self.simi.setdefault(i, dict())
            for j, rate in j_dict.items():
                self.simi[i][j] = rate/np.sqrt(float(norm[i] * norm[j]))

    def cacl_simi(self):
        if self.type == 'item':
            self.calc_simi_cos(self.user_item)
        elif self.type == 'user':
            self.calc_simi_cos(self.item_user)

    def recommend_item(self, id):
        rank = dict()
        stop_item = [x for x, y in self.user_item[id]]
        # print self.user_item[id]
        # print sorted(self.test[id])

        for u_item, u_rate in self.user_item[id]:
            for v, item_simi in sorted(self.simi[u_item].items(), key=lambda x:x[1], reverse=True)[:self.k]:
                if v not in stop_item:
                    rank[v] = rank.setdefault(v, 0) + item_simi * u_rate
        rank = list(sorted(rank.items(), key=lambda x: x[1], reverse=True))
        
        # hit = 0
        # for item_id, pui in rank[:10]:
        #     print 'movie: ', self.item_map[str(item_id)][0], 'rank: ', pui, ' item_id',item_id
        #     if item_id in self.test[id]:
        #         hit += 1
        # print 'hit: ', hit
        return rank

    def precision(self):
        return self.cacl_pre_or_recall(2)

    def recall(self):
        return self.cacl_pre_or_recall()

    # 默认计算召回率
    def cacl_pre_or_recall(self, flag=1):
        hit = 0
        all = 0
        recommend = self.recommend_item
        if self.type == 'user':
            return 0
        for user, td in self.test.items():
            rank = recommend(user)
            for item, res in rank[:self.N]:
                if item in td:
                    hit += 1
            if flag == 1:
                all += len(td)
            else:
                all += self.N
        return hit * 1.0 / all

    def coverage(self):
        all_items = set()
        recommend_item = set()
        recommend = self.recommend_item
        if self.type == 'user':
            return 0
        for user, td in self.test.items():
            all_items |= set(td)
            rank = recommend(user)
            for item, rate in rank:
                if item in all_items:
                    recommend_item.add(item)
        return float(len(recommend_item))/len(all_items)

if __name__ == '__main__':
    itemCF = CF(8, 'item')
    itemCF.read_file('../data/ml-100k/u.data')
    itemCF.cacl_simi()
    rank = itemCF.recommend_item(447)
    print itemCF.precision()
    print itemCF.recall()
    print itemCF.coverage()