# -*- coding=utf-8 -*
import urllib
import urllib2
from bs4 import BeautifulSoup
import logging
import traceback

def writeFile(str):
    with open("movie.html", 'w') as f:
        f.write(str)

def readFile():
    with open("movie.html") as f:
        return f.read()

class spiderStatus:
    timeout = 0
    htmlerror = 1
    normal = 2

class movieSpider:
    def __init__(self):
        self.fail_movie = []
        self.cur_movie = None
        self.cur_status = spiderStatus.normal

    def search(self, movie_name):
        logger = logging.getLogger('spider')
        logger.info("begin search <<%s>>" % movie_name)
        url = 'http://www.imdb.com/find'
        data = {
            'ref_': 'nv_sr_fn',
            'q': movie_name,
            's': 'all',
        }
        data = urllib.urlencode(data)
        req = urllib2.Request(url=url, data=data)
        res = {}
        try:
            html = urllib2.urlopen(req, timeout=6).read()
            # html = readFile()
            soup = BeautifulSoup(html)
            divs = soup.find_all('div', class_='findSection')
            for div in divs:
                titile = div.find('h3').contents[1]
                if titile == 'Titles':
                    movie_url = div.find('table').find('a')
                    res['url'] = 'http://www.imdb.com' + movie_url['href']
        except Exception, e:
            print 'search url of spider timeout: ', e.message
            logger.warning("timeout.", exc_info=True)
            res['name'] = movie_name
            self.fail_movie.append(self.cur_movie)
        # writeFile(html)
        logger.info("end search <<%s>>" % movie_name)
        return res

    def find_movie_info(self, soup):
        logger = logging.getLogger('spider')
        try:
            # summary
            divs = soup.find_all('div', class_='plot_summary_wrapper')[0]
            summary_div = divs.find('div', class_='summary_text')
            # print 'summary_div: \n', summary_div
            # img_url
            img_div = soup.find('div', class_ = 'poster')
            img_url = img_div.find('img')['src']
            # print 'img_div: \n', img_div
            # star, diretion
            for div in divs.children:
                if div.name == 'div' and div['class'][0] == 'plot_summary':
                    credit_div = div.find_all('div', class_='credit_summary_item')
                    break
            movie_star = []
            director = ''
            for div in credit_div:
                if div.find('h4').string == 'Stars:':
                    for a in div.find_all('a'):
                        movie_star.append(a.contents[0].string)
                if div.find('h4').string == 'Director:':
                    for a in div.find_all('a'):
                        director = a.contents[0].string
            # type
            movie_type = self.get_type(soup)
        except Exception, e:
            print 'html error. ', e.message
            logger.error('html error. ', exc_info=True)
            self.fail_movie.append(self.cur_movie)
            self.cur_status = spiderStatus.htmlerror
            return None
        movie_info = {}
        movie_star.pop()
        movie_info['stars'] = movie_star
        movie_info['director'] = director
        movie_info['summary'] = summary_div.get_text().strip()
        movie_info['img_url'] = img_url
        movie_info["type"] = movie_type
        return movie_info

    def get_type(self, soup):
        try:
            divs = soup.find_all('div', class_='title_wrapper')[0]
            div = divs.find('div', class_='subtext')
            a = div.find_all('a')
            lable = []
            for i in range(len(a)-1):
                lable.append(a[i].string)
        except Exception, e:
            raise Exception("spider: get movie type error.\n" + e.message)
            return None
        return lable

    def get_html(self, req):
        logger = logging.getLogger('spider')
        html = None
        try:
            html = urllib2.urlopen(req, timeout=6).read()
        except Exception, e:
            print 'get_html of spider timeout.', e.message
            logger.error('get_html of spider timeout.', exc_info=True)
            self.fail_movie.append(self.cur_movie)
            self.cur_status = spiderStatus.timeout
        return html

    def spider(self, url):
        req = urllib2.Request(url)
        html = self.get_html(req)
        if html is None:
            return None
        # html = readFile()
        soup = BeautifulSoup(html)
        movie_info = self.find_movie_info(soup)
        # writeFile(html)
        return movie_info

    def get_movie_info2(self, movie):
        self.cur_movie = movie[1]
        print movie
        name = movie[1]
        age = name.split('(')[1].split(')')[0]
        res = self.search('Scream of Stone (Schrei aus Stein) (1991)')
        print res
        if 'url' in res:
            movie_info = self.spider(res['url'])
            if movie_info is not None:
                movie_info['age'] = age
        return movie_info

    def make_spider_res(self, url, name):
        for i in range(3):
            movie_info = self.spider(url)
            if movie_info is not None:
                age = name.split('(')[1].split(')')[0]
                movie_info['age'] = age
                break
            elif self.cur_status == spiderStatus.htmlerror:
                break
            self.cur_status = spiderStatus.normal
        return movie_info

    def get_movie_info(self, movie):
        import logging
        logger = logging.getLogger('spider')
        logger.info('start spider %s' % movie[1])
        url = movie[3]
        self.cur_movie = movie[1]
        movie_info = self.make_spider_res(url, self.cur_movie)
        if movie_info is None and self.cur_status != spiderStatus.timeout:
            for i in range(3):
                res = self.search(self.cur_movie)
                if 'url' in res:
                    movie_info = self.make_spider_res(res['url'], self.cur_movie)
                    break
        if movie_info is not None:
            movie_info['name'] = self.cur_movie
            movie_info['_id'] = movie[0]
            logger.info("success spider %s" % movie[1])
        else:
            logger.info("fail spider %s" % movie[1])
        return movie_info
