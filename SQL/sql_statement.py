# -*- coding:utf-8 -*-


def get_all():
    return "select * from user"

def get_user_pwd(account):
    return "select pwd from user where account='%s'" % account

# user: [nick, age, sex, work, account, pwd]
def registe_user(user):
    return """insert into user(nick, age, sex, work, account, pwd) 
              values('%s', %s, '%s', '%s', '%s', '%s')""" % \
           (user[0], user[1], user[2], user[3], user[4], user[5])

def insert_behavior():
    return """
        insert into behavior(user_id, item_id, rate, time) 
        values(%s, %s, %s, %s)
    """

def insert_movie():
    return """
        insert into movies(id, name, time, url)
        values(%s, %s, %s, %s)
    """

def insert_user(user):
    return """
        insert into user(nick, age, sex, work, account, pwd)
        values('%s', %s, '%s', '%s', '%s', '%s')
    """ % (user['nick'], user['age'], user['sex'], \
           user['job'],user['account'], user['pwd'])

def get_all(table):
    return """
        select * from %s
    """ % table


def get_cnt(table):
    return """select count(*) from %s""" % table

def get_cnt_with_work(table):
    return """select work, count(*) from %s group by work""" % table


def get_movie_name_by_id(id):
    return """select """


def get_user_by_act(account):
    return """select * from user where account='%s'""" % account


def alter_pwd(account, pwd):
    return """update user set pwd='%s' where account='%s'""" % (account, pwd)


# 用户行为计数
def user_behavior_cnt(user_id):
    return """
            select count(user_id) from behavior 
            where user_id=%s 
            group by user_id
            """ % str(user_id)


def movie_behavior_cnt(movie_id):
    return """
        select count(item_id) from behavior
        where item_id=%s 
        group by item_id
    """ % str(movie_id)


def update_user_behavior(user_id, item_id, score):
    return """
        update behavior
        set rate=%s
        where user_id=%s and item_id=%s
    """ % (score, user_id, item_id)


def get_movie_score(user_id, item_id):
    return """
        select rate from behavior 
        where user_id=%s and item_id=%s 
    """ % (user_id, item_id)


def get_user_by_id(user_id):
    return """select * from user where id=%s""" % user_id