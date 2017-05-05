# -*- coding=utf-8 -*-
from pymongo import MongoClient
import logging


def get_collection(col):
    client = MongoClient('localhost', 27017)
    if col == 'movie':
        return client.rs.movie
    elif col == 'webLog':
        return client.rs.webLog


def insert(col, data):
    col.insert(data)


def find(col, cond={}, field={}):
    logger = logging.getLogger()
    logging.info('find %s by' % str(col) + str(cond))
    try:
        if len(field) == 0:
            return col.find(cond)
        else:
            return col.find(cond, field)
    except Exception, e:
        logger.error('find %s by' % str(col) + str(cond), exc_info=True)
        return None

if __name__ == '__main__':
    res= find(get_collection('movie'))
