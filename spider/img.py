# -*- coding=utf-8 -*
import requests
import traceback
import logging


class imgSpider:
    def get_imgs(self, movie):
        logger = logging.getLogger('spider')
        logger.info("start loaddown img of %s" % movie['name'])
        try:
            pic = requests.get(movie['img_url'], timeout=10)
            logger.error("success: loaddown img of %s" % movie['name'])
        except Exception, e:
            logger.error("fail: loaddown img of %s" % movie['name'])
            print '【错误】当前图片无法下载'
            return None
        return pic
