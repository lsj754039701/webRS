from SQL import *


def login(account, pwd):
    user_pwd = fetchone(sql_statement.get_user_pwd(account))
    if len(user_pwd) == 0:
        return False
    return pwd == user_pwd[0]


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


def insert_user(user):
    return update(sql_statement.insert_user(user))


def find_user_by_account(account):
    return fetchone(sql_statement.get_user_by_act(account))


def alter_pwd(account, pwd):
    return update(sql_statement.alter_pwd(account, pwd))


def is_new_user(user_id):
    cnt = fetchone(sql_statement.user_behavior_cnt(user_id))
    if cnt is None or cnt[0] < 30:
        return True
    return False


def is_new_movie(movie_id):
    cnt = fetchone(sql_statement.movie_behavior_cnt(movie_id))
    if cnt is None or cnt[0] < 30:
        return True
    return False


def get_movie_cnt(movie_id):
    cnt = fetchone(sql_statement.movie_behavior_cnt(movie_id))
    if cnt is None:
        return 0
    else:
        return cnt[0]


def update_user_behavior(user_id, item_id, score):
    return update(sql_statement.update_user_behavior(user_id, item_id, score))


def get_movie_score(user_id, item_id):
    return fetchone(sql_statement.get_movie_score(user_id, item_id))


def is_buy(user_id, item_id):
    score = get_movie_score(user_id, item_id)
    if score is None:
        return False
    else:
        return True


def can_score(user_id, item_id):
    score = get_movie_score(user_id, item_id)
    if score is not None and score[0] == 0:
        return True
    else:
        return False


def get_user_by_id(user_id):
    return fetchone(sql_statement.get_user_by_id(user_id))