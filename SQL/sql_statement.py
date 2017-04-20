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

def get_all(table):
    return """
        select * from %s
    """ % table


def get_cnt(table):
    return """select count(*) from %s""" % table

def get_cnt_with_work(table):
    return """select work, count(*) from %s group by work""" % table