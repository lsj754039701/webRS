# -*- coding=utf-8 -*-
from SQL import *
from pymongo import MongoClient

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
    return list(mongo_sql.find(mongo_sql.get_collection('movie'), {'_id': id}))


