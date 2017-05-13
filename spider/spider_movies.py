import model
import multiprocessing
import movies
import img
from pymongo import MongoClient


def fun(movie, k):
    from spider import movies
    import model
    print 'start spider %s' % movie
    s = movies.movieSpider()
    # res = s.get_movie_info(movie)
    res = s.add_movie(movie)
    print 'it is ', res
    if res is not None:
        res['_id'] = k
        print 'k: ', k
        model.mongo.insert_movie(res)
        load_img(res)
        print res
        client = MongoClient('localhost', 27017)
        success = client.rs.success
        success.insert({'name': movie})
    else:
        client = MongoClient('localhost', 27017)
        fail = client.rs.fail
        fail.insert({'name': movie})


def spider_movies(all_movies):
    pool = multiprocessing.Pool(processes=30)
    # all_movies = model.get_all_movie()
    num = model.mongo.get_movies_num()
    k = num + 1000
    for movie in all_movies:
        k += 1
        pool.apply_async(fun, args=(movie, k))
    pool.close()
    pool.join()
    client = MongoClient('localhost', 27017)
    success = client.rs.success
    res = success.find()
    # success.drop()
    return list(res)
    # print 'end'


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


def load_img(movie):
    import img
    spider = img.imgSpider()
    pic = spider.get_imgs(movie)
    if pic is None:
        client = MongoClient('localhost', 27017)
        fail = client.rs.fail
        fail.insert({'img': movie['_id']})
    else:
        localtion = "/home/zll/PycharmProjects/RS/static/images/movies/" + str(movie['_id']) + ".jpg"
        # localtion = '/home/zll/pic2/' + str(movie['_id']) + ".jpg"
        fp = open(localtion, "wb")
        fp.write(pic.content)
        fp.close()

def spider_imgs(all_movies):
    # movies = model.mongo.find_all_movies()
    pool = multiprocessing.Pool(processes=30)
    for movie in all_movies:
        load_img(movie)



