import multiprocessing
from multiprocessing import Queue
import time
d = 0

def fun1(q):
    q.put(1)
    q.put(2)
    time.sleep(3)
    print 'put', q.empty()
    q.put(3)
    q.put(4)

def fun2(q):

    print 'get', q.empty()
    while not q.empty():
        print 'begin:'
        a = q.get()
        print 'get: ',a
        time.sleep(1)

    # print q.get()

if __name__ == "__main__":
    q = Queue()
    p1 = multiprocessing.Process(target=fun1, args=(q, ))
    p2 = multiprocessing.Process(target=fun2, args=(q, ))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print 'end'

