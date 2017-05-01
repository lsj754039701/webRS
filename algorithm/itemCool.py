# -*- coding=utf-8 -*
import numpy as np
from numpy import linalg
import model
import until

def load_movie():
    with open("/home/zll/PycharmProjects/RS/data/ml-100k/movies.dat") as f:
        all_movies = {}
        for line in f.readlines():
            line = line.strip()
            split_data = line.split('::')
            all_movies.setdefault(split_data[1], {})['type'] = split_data[2].split('|')
        return all_movies



class itemCool():
    # 默认给三个用户推荐新电影
    def __init__(self, k=3):
        self.k = 3
        all_movies = model.mongo.find_all_movies()
        self.movies = {}
        for movie in all_movies:
            self.movies[movie['_id']] = movie
        self.type_dict = self.get_type_dict()
        self.user_vec = {}
        self.__create_user_model()

    def get_type_dict(self):
        movie_dict = set([])
        for movie in self.movies.values():
            movie_dict |= set(movie['type'])
        return list(movie_dict)

    def get_type_vec(self, movie):
        type_vec = np.zeros(len(self.type_dict))
        for type in movie['type']:
            type_vec[self.type_dict.index(type)] = 1
        return type_vec

    def __get_user_type_vec(self, rates):
        user_type_vec = np.zeros(len(self.type_dict))
        hx_cnt = np.zeros(len(self.type_dict))
        for item_id, rate in rates:
            if item_id in self.movies:
                movie = self.movies[item_id]
                for type in movie['type']:
                    hx_cnt[self.type_dict.index(type)] += 1
                    user_type_vec[self.type_dict.index(type)] += rate

        for i in range(len(hx_cnt)):
            if hx_cnt[i] == 0:
                hx_cnt[i] = -1
        user_type_vec = np.divide(user_type_vec, hx_cnt)
        return user_type_vec

    def __create_user_model(self):
        behaviors = model.get_all_behavior()
        user_rate = {}
        for behavior in behaviors:
            user_rate.setdefault(behavior[1], []).append([behavior[2], behavior[3]])
        for user_id, rate in user_rate.items():
            self.user_vec[user_id] = self.__get_user_type_vec(rate)

    def __calc_sim(self, movie_vec, user_vec):
        norm = linalg.norm(movie_vec, 2) * linalg.norm(user_vec, 2)
        return np.dot(user_vec , movie_vec) / norm

    def recommend(self, movie):
        queue = until.priorityQueue(self.k, lambda x: x[1])
        movie_vec = self.get_type_vec(movie)
        mx = 0
        for user_id, user_vec in self.user_vec.items():
            queue.push([user_id, self.__calc_sim(movie_vec, user_vec)])
            mx = max( self.__calc_sim(movie_vec, user_vec), mx)
        return queue.get_all_num()

