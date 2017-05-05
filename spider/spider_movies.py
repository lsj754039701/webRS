import model
import multiprocessing
import movies
import img
# from spider import *
# s = movies.movieSpider()
# print s.spider("http://us.imdb.com/M/title-exact?Schrei%20aus%20Stein%20(1991)")
# print s.spider("http://us.imdb.com/M/title-exact?Sweet%20Nothing%20(1995)")
# print s.get_movie_info("a")

def fun(movie):
    from spider import *
    from model import *
    print 'start spider %s' % movie[1]
    s = movies.movieSpider()
    res = s.get_movie_info(movie)
    # print 'it is ', res
    if res is not None:
        mongo.insert_movie(res)
    else:
        name = '/home/zll/PycharmProjects/spdier/%s' % movie[1]
        with open(name) as f:
            if len(s.fail_movie) > 0:
                f.write(s.fail_movie[0] + '\n')


def spider_movies():
    pool = multiprocessing.Pool(processes=30)
    all_movies = model.get_all_movie()
    k = 0
    for movie in all_movies:
        # k += 1
        # if k > 3:
        #     break
        # print movie
        pool.apply_async(fun, args=(movie,))
    pool.close()
    pool.join()
    print 'end'



def img_process(movie, lock):
    print 'start spider img of %s' % movie['name']
    spider = img.imgSpider()
    pic = spider.get_imgs(movie)
    if pic is None:
        lock.acquire()
        with open("/home/zll/pic/fail.txt", "w") as f:
            f.write(movie["_id"])
        lock.release()
    else:
        lock.acquire()
        localtion = "/home/zll/pic/" + str(movie['_id']) + ".jpg"
        fp = open(localtion, "wb")
        fp.write(pic.content)
        fp.close()
        lock.release()


def spider_imgs():
    movies = model.mongo.find_all_movies()
    pool = multiprocessing.Pool(processes=30)
    manager = multiprocessing.Manager()
    lock = manager.Lock()
    spider = img.imgSpider()
    for movie in movies:
        pic = spider.get_imgs(movie)
        if pic is None:
            with open("/home/zll/pic/fail.txt", "w") as f:
                f.write(str(movie["_id"]) + '\n')
        else:
            localtion = "/home/zll/pic/" + str(movie['_id']) + ".jpg"
            fp = open(localtion, "wb")
            fp.write(pic.content)
            fp.close()



