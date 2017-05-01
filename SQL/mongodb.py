# -*- coding=utf-8 -*-
from pymongo import MongoClient
import logging


def get_collection(col):
    client = MongoClient('localhost', 27017)
    if col == 'movie':
        return client.rs.movie


def insert(col, data):
    col.insert(data)


def find(col, cond={}):
    logger = logging.getLogger()
    logging.info('find %s by' % str(col) + str(cond))
    try:
        return col.find(cond)
    except Exception, e:
        logging.error('find %s by' % str(col) + str(cond), exc_info=True)
        return None

if __name__ == '__main__':
    res= find(get_collection('movie'))
