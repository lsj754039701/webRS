# -*- coding=utf-8 -*-
from SQL import *
from pymongo import MongoClient
import model

def insert_movie(movie):
    client = MongoClient('localhost', 27017)
    rs = client.rs
    rs.movie.insert(movie)


def find_all_movies():
    try:
        client = MongoClient('localhost', 27017)
        movies = client.rs.movie
        return movies.find()
    except Exception, e:
        print e.message


def find_movie_by_id(id):
    return list(mongo_sql.find(mongo_sql.get_collection('movie'), cond={'_id': id}))


def find_movie_by_name(name):
    return list(mongo_sql.find(mongo_sql.get_collection('movie'), cond={'name': name}))


def find_new_movies():
    new_movies = []
    moviesID = list(mongo_sql.find(mongo_sql.get_collection('movie'), cond={}, field={'_id': 1}))
    for movie_id in moviesID:
        if model.is_new_movie(movie_id['_id']):
            movie = find_movie_by_id(movie_id['_id'])[0]
            new_movies.append(movie)
    return new_movies


def insert_web_log(data):
    mongo_sql.insert(mongo_sql.get_collection('webLog'), data)


def find_web_log(cond):
    return mongo_sql.find(mongo_sql.get_collection('webLog'), cond=cond)


def get_movies_num():
    return mongo_sql.get_collection('movie').find().count()


def save_movie(movie):
    return mongo_sql.save(mongo_sql.get_collection('movie'), movie)