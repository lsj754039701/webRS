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
    # 默认给十个用户推荐新电影
    def __init__(self, k=10, n=6):
        self.k = k
        self.N = n
        all_movies = model.mongo.find_all_movies()
        self.movies = {}
        for movie in all_movies:
            self.movies[movie['_id']] = movie
        self.type_dict = self.get_type_dict()
        self.star_dict = self.get_star_dict()
        self.user_vec = {}
        self.star_user_vec = {}
        self.__create_user_model()
        self.new_item = model.mongo.find_new_movies()
        self.item_rec_user = {}
        self.rec_init()

    def get_type_dict(self):
        return self.__get_dict('type')

    def get_star_dict(self):
        return self.__get_dict('stars')

    def __get_dict(self, field):
        movie_dict = set([])
        for movie in self.movies.values():
            movie_dict |= set(movie[field])
        return list(movie_dict)

    def get_movie_type_vec(self, movie):
        type_vec = np.zeros(len(self.type_dict))
        for type in movie['type']:
            type_vec[self.type_dict.index(type)] = 1
        return type_vec

    def get_movie_star_vec(self, movie):
        star_vec = np.zeros(len(self.star_dict))
        for star in movie['stars']:
            star_vec[self.star_dict.index(star)] = 1
        return star_vec

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

    def __get_user_star_vec(self, rates):
        user_star_vec = np.zeros(len(self.star_dict))
        hx_cnt = np.zeros(len(self.star_dict))
        for item_id, rate in rates:
            if item_id in self.movies:
                movie = self.movies[item_id]
                for star in movie['stars']:
                    hx_cnt[self.star_dict.index(star)] += 1
                    user_star_vec[self.star_dict.index(star)] += rate
        # avoid to divid zero
        for i in range(len(hx_cnt)):
            if hx_cnt[i] == 0:
                hx_cnt[i] = -1
        user_star_vec = np.divide(user_star_vec, hx_cnt)
        return user_star_vec

    def __create_user_model(self):
        behaviors = model.get_all_behavior()
        user_rate = {}
        for behavior in behaviors:
            user_rate.setdefault(behavior[1], []).append([behavior[2], behavior[3]])
        for user_id, rate in user_rate.items():
            self.user_vec[user_id] = self.__get_user_type_vec(rate)
            self.star_user_vec[user_id] = self.__get_user_star_vec(rate)

    def __calc_sim(self, movie_vec, user_vec):
        norm = linalg.norm(movie_vec, 2) * linalg.norm(user_vec, 2)
        if norm == 0: return 0
        return np.dot(user_vec, movie_vec) / norm

    def __recommend(self, movie):
        queue = until.priorityQueue(self.k, lambda x: x[1])
        movie_type_vec = self.get_movie_type_vec(movie)
        movie_star_vec = self.get_movie_star_vec(movie)
        mx = 0
        for user_id, user_vec in self.user_vec.items():
            type_rate = self.__calc_sim(movie_type_vec, user_vec)
            star_rate = self.__calc_sim(movie_star_vec, self.star_user_vec[user_id])
            queue.push([user_id, 0.5 * type_rate + star_rate])
            # mx = max( self.__calc_sim(movie_vec, user_vec), mx)
        return queue.get_all_num()

    def rec_init(self):
        for movie in self.new_item:
            users = self.__recommend(movie)
            self.item_rec_user[movie['_id']] = users
        # for key, val in self.item_rec_user.items():
        #     print key, "=> ", val

    def recommend(self, user_id):
        res = []
        for movie_id, users in self.item_rec_user.items():
            for user, rate in users:
                if user_id == user:
                    res.append((movie_id, rate))
        return sorted(res, key=lambda x: x[1], reverse=True)[:self.N]