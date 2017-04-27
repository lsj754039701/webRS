# -*- coding=utf-8 -*
import urllib
import urllib2
from bs4 import BeautifulSoup
import model
import logging

def writeFile(str):
    with open("movie.html", 'w') as f:
        f.write(str)

def readFile():
    with open("movie.html") as f:
        return f.read()

class movieSpider:
    def __init__(self):
        self.fail_movie = []
        self.cur_movie = None

    def search(self, movie_name):
        logger = logging.getLogger()
        logger.info("begin search <<%s>>" % movie_name)
        url = 'http://www.imdb.com/find?ref_=nv_sr_fn&q=B.+Monkey+%281998%29&s=all'
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
            print 'timeout: ', e.message
            logger.warning("timeout.", exc_info=True)
            res['name'] = movie_name
            self.fail_movie.append(self.cur_movie)
        # writeFile(html)
        logger.info("end search <<%s>>" % movie_name)
        return res

    def find_movie_info(self, soup):
        try:
            # summary
            divs = soup.find_all('div', class_='plot_summary_wrapper')[0]
            summary_div = divs.find('div', class_='summary_text')
            # img_url
            img_div = soup.find('div', class_ = 'minPosterWithPlotSummaryHeight')
            img_url = img_div.find('img')['src']
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
        except Exception, e:
            print e.message
            return None
        movie_info = {}
        movie_star.pop()
        movie_info['stars'] = movie_star
        movie_info['director'] = director
        movie_info['summary'] = str(summary_div.string).strip()
        movie_info['img_url'] = img_url
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
            print e.message
            return None
        return lable

    def get_html(self, req):
        html = None
        try:
            html = urllib2.urlopen(req, timeout=6).read()
        except Exception, e:
            print 'spider timeout.', e.message
            self.fail_movie.append(self.cur_movie)
        return html

    def spider(self, url):
        req = urllib2.Request(url)
        html = self.get_html(req)
        if html is None:
            return None
        # html = readFile()
        soup = BeautifulSoup(html)
        movie_info = self.find_movie_info(soup)
        movie_info['type'] = self.get_type(soup)
        # writeFile(html)
        return movie_info

    def get_movie_info(self):
        movies = model.get_all_movie()
        k = 0
        all_movie = {}
        for movie in movies:
            k += 1
            if k > 20:
                break
            self.cur_movie = movie[1]
            print movie[1]
            s = movie[1]
            age = s.split('(')[1].split(')')[0]
            res = self.search('B. Monkey (1998)')
            print res
            if 'url' in res:
                movie_info = self.spider(res['url'])
                if movie_info is not None:
                    movie_info['age'] = age
                    all_movie[movie[1]] = movie_info
        print self.fail_movie
        return all_movie