# -*- coding=utf-8 -*
import requests
import traceback


class imgSpider:
    def get_imgs(self, movie):
        try:
            pic = requests.get(movie['img_url'], timeout=10)
        except Exception, e:
            print '【错误】当前图片无法下载'
            return None
        return pic
