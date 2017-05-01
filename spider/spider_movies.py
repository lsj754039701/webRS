import model
import multiprocessing
# from spider import *
# s = movies.movieSpider()
# print s.spider("http://us.imdb.com/M/title-exact?Schrei%20aus%20Stein%20(1991)")
# print s.spider("http://us.imdb.com/M/title-exact?Sweet%20Nothing%20(1995)")
# print s.get_movie_info("a")


if __name__ == '__main__':
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

    k = 0
    pool = multiprocessing.Pool(processes=30)
    all_movies = model.get_all_movie()

    for movie in all_movies:
        # k += 1
        # if k > 3:
        #     break
        # print movie
        pool.apply_async(fun, args=(movie, ))
    pool.close()
    pool.join()
    print 'end'
