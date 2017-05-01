# -*- coding=utf-8 -*-
import MySQLdb
from DBUtils.PooledDB import PooledDB
from ConfigParser import ConfigParser


class sqlconf:
    def __init__(self):
        config = ConfigParser()
        config.read("conf/sql.conf")
        self.host = config.get('db', 'host')
        self.port = config.get('db', 'port')
        self.user = config.get('db', 'user')
        self.pwd = config.get('db', 'pwd')
        self.dbname = config.get('db', 'dbname')

conf = sqlconf()
pool = PooledDB(MySQLdb, 5, host=conf.host, port=int(conf.port),
                db=conf.dbname, user=conf.user, passwd=conf.pwd, charset='utf8')


if __name__ == "__main__":
    conn = pool.connection()
    cur = conn.cursor()
    cur.execute("select * from user")
    r = cur.fetchall()
    print r

