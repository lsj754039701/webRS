# -*- coding=utf-8 -*-
from pool import *
import logging


def update(sql_str):
    logger = logging.getLogger()
    logger.info('begin update,sql_str: %s' % sql_str)
    conn = pool.connection()
    cur = conn.cursor()
    flag =True
    try:
        cur.execute(sql_str)
        conn.commit()
    except Exception, e:
        logger.error('update error.', exc_info=True)
        flag = False
        conn.rollback()
    conn.close()
    return flag


def update_many(sql_str, datas):
    logger = logging.getLogger()
    logger.info('begin update_many,sql_str: %s' % sql_str)
    conn = pool.connection()
    cur = conn.cursor()
    flag =True
    try:
        cur.executemany(sql_str, datas)
        conn.commit()
    except Exception, e:
        logger.error('update_many error.', exc_info=True)
        flag = False
        conn.rollback()
    conn.close()
    logger.info('end update_many.')
    return flag


def fetchall(sql_str):
    logger = logging.getLogger()
    logger.info('begin fetchall, sql_str: %s' % sql_str)
    res = ""
    try:
        conn = pool.connection()
        cur = conn.cursor()
        cur.execute(sql_str)
        res = cur.fetchall()
    except Exception, e:
        logger.error("fetchall error.", exc_info=True)
    logger.info("end fetchall")
    conn.close()
    return res


def fetchone(sql_str):
    logger = logging.getLogger()
    logger.info('begin fetchone,sql_str: %s' % sql_str)
    res = None
    try:
        conn = pool.connection()
        cur = conn.cursor()
        cur.execute(sql_str)
        res = cur.fetchone()
    except Exception, e:
        print 'fetchone error.%s' % sql_str, e.message
        logger.error("fetchone error.", exc_info=True)
    logger.info("end fetchone")
    conn.close()
    return res

