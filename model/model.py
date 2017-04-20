from SQL import *


def login(account, pwd):
    user_pwd = fetchone(sql_statement.get_user_pwd(account))[0]
    return pwd == user_pwd


def registe(users):
    update(sql_statement.registe_user(users))


def insert_behaviors(datas):
    update_many(sql_statement.insert_behavior(), datas)


def insert_movies(movies):
    update_many(sql_statement.insert_movie(), movies)


def get_cnt_by_age():
    table = "user"
    res = []
    teen = fetchone(sql_statement.get_cnt(table) + " where age<20")[0]
    midlife = fetchone(sql_statement.get_cnt(table) + " where age>=20 and age<50")[0]
    old = fetchone(sql_statement.get_cnt(table) + " where age>=50")[0]
    res.append(teen)
    res.append(midlife)
    res.append(old)
    for i in range(len(res)):
        if res[i] != "":
            res[i] = int(res[i])
        else:
            res[i] = 0
    return res


def get_cnt_by_sex():
    table = "user"
    res = []
    girl = fetchone(sql_statement.get_cnt(table) + " where sex='F'")[0]
    boy = fetchone(sql_statement.get_cnt(table) + " where sex='M'")[0]
    res.append(girl)
    res.append(boy)
    for i in range(len(res)):
        if res[i] != "":
            res[i] = int(res[i])
        else:
            res[i] = 0
    return res


def get_cnt_by_job():
    table = "user"
    return fetchall(sql_statement.get_cnt_with_work(table))


def get_all_movie():
    return fetchall(sql_statement.get_all("movies"))


def get_all_user():
    return fetchall(sql_statement.get_all("user"))

def get_all_behavior():
    return fetchall(sql_statement.get_all("behavior"))


