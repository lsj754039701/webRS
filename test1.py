# -*- coding=utf-8 -*-
import multiprocessing
from multiprocessing import Queue
import time
import logging.config
d = 0

def fun1(q):
    q.put(1)
    q.put(2)
    time.sleep(3)
    print 'put', q.empty()
    q.put(3)
    q.put(4)

def fun2(q):

    print 'get', q.empty()
    while not q.empty():
        print 'begin:'
        a = q.get()
        print 'get: ',a
        time.sleep(1)

    # print q.get()

def insert_user():
    name = 'data/ml-100k/u.user'
    with open(name) as f:
        i = 0
        for line in f.readlines():
            user_info = line.split('|')
            user = ['zll', user_info[1], user_info[2], user_info[3], 'zll' + str(i), 'zll']
            model.registe(user)
            i += 1

def insert_behavior():
    name = 'data/ml-100k/u.data'
    with open(name) as f:
        i = 0
        datas = []
        for line in f.readlines():
            data = line.split('\t')
            data[3] = data[3].split('\n')[0]
            datas.append(tuple(data))
        # print datas
        model.insert_behaviors(datas)

def insert_movies():
    name1 = 'data/ml-100k/u.item'
    name2 = 'data/ml-100k/movies.dat'
    m1 = []
    m2 = []
    with open(name1) as f:
        for line in f.readlines():
            data = line.split('|')[:5]
            m1.append(data)
    print m1[1]
    with open(name2) as f:
        for line in f.readlines():
            data = line.split('::')
            m2.append(data)
    print m2[1]
    for x in m1:
        for y in m2:
            if x[1] == y[1]:
                x.append(y[2].split('\n')[0])
    mouth = {
        'Jan': 01, 'Feb': 02, 'Mar': 03, 'Apr': 04, 'May': 05,
        'Jun': 06, 'Jul': 07, 'Aug': 8, 'Sep': 9, 'Oct': 10,
        'Nov': 11, 'Dec': 12
    }
    for x in m1:
        date = x[2].split('-')
        if '' in date:
            pass
        else:
            date[1] = mouth[date[1]]
            date.reverse()
            date[1] = str(date[1])
            x[2] = '-'.join(date)
        x.pop(3)
        if len(x) != 5:
           pass
        else:
            x.pop(len(x)-1)
    print m1[266]
    m1.pop(266)

    model.insert_movies(m1)


logging.config.fileConfig('conf/log.conf')
import model
from SQL import pool
if __name__ == "__main__":
    insert_movies()



