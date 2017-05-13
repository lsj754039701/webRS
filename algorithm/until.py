# -*- coding=utf-8 -*
import re
import model
import time
import datetime
import threading


lock = threading.Lock()
scored = {}
buyed = []
#
# class process_queue:
#     queue = multiprocessing.Queue()
#     itemCF = get_itemCF()
#     userCF = get_userCF()
#     user_cool = get_user_cool()
#     item_cool = get_item_cool()
#
#     @staticmethod
#     def get():
#         if not process_queue.queue.empty():
#             print "queue is not empty"
#             new_res = process_queue.queue.get()
#             process_queue.itemCF = new_res[0]
#             process_queue.userCF = new_res[1]
#             process_queue.user_cool = new_res[2]
#             process_queue.item_cool = new_res[3]
#         return process_queue.itemCF, process_queue.userCF, process_queue.user_cool, process_queue.item_cool
#
#


class priorityQueue:
    def __init__(self, n, fun):
        self.__q = []
        self.n = n
        self.fun = fun

    def min(self):
        mn = 100000
        idx = 0
        for i in range(len(self.__q)):
            if mn > self.fun(self.__q[i]):
                mn = self.fun(self.__q[i])
                idx = i
        return mn, idx

    def push(self, item):
        x = self.fun(item)
        if len(self.__q) < self.n:
            self.__q.append(item)
        else:
            mn, idx = self.min()
            if x > mn:
                self.__q[idx] = item
    
    def get_all_num(self):
        return self.__q


class webLog:
    @staticmethod
    def web_mongo():
        pal = re.compile(r"\[(.*?) \[.*?\].*?\] INFO: (.*?) \[(.*?)\] (.*)")
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        filename = "log/webLog/web" + date
        with open("log/web.log") as f:
            for line in f.readlines():
                res = pal.search(line)
                log_time = res.group(1)
                req_type = res.group(2)
                behavior_type = res.group(3)
                data = res.group(4)
                timestamp = time.mktime(time.strptime(log_time, "%Y-%m-%d %H:%M:%S"))
                behavior = {}
                behavior['timestamp'] = int(timestamp)
                behavior['type'] = req_type
                behavior['user_id'] = data.split(' ')[0].split(':')[1]
                if behavior_type == 'buyMovie':
                    behavior['behavior'] = {
                        'type': behavior_type,
                        'movie_id': data.split(' ')[1].split(':')[1]
                    }
                elif behavior_type == 'scoreMovie':
                    behavior['behavior'] = {
                        'type': behavior_type,
                        'movie_id': data.split(' ')[1].split(':')[1],
                        'score': data.split(' ')[2].split(':')[1]
                    }
                else:
                    behavior['behavior'] = {
                        'type': behavior_type
                    }
                # print behavior
                model.mongo.insert_web_log(behavior)

    @staticmethod
    def add_behavior():
        today = datetime.datetime.now()
        delta = datetime.timedelta(days=-1)
        yesterday = today + delta
        today = today.strftime("%Y-%m-%d")
        yesterday = yesterday.strftime("%Y-%m-%d")
        today = time.mktime(time.strptime(today, "%Y-%m-%d"))
        yesterday = time.mktime(time.strptime(yesterday, "%Y-%m-%d"))
        cond = {'timestamp': {'$gte': int(yesterday), '$lt': int(today + 93827200)}}
        logs = model.mongo.find_web_log(cond)
        scores = []
        buys = []
        for log in logs:
            user_id = log['user_id']
            timestamp = log['timestamp']
            if log['behavior']['type'] == 'scoreMovie':
                movie_id = log['behavior']['movie_id']
                score = log['behavior']['score']
                scores.append((user_id, movie_id, score, timestamp))
            elif log['behavior']['type'] == 'buyMovie':
                movie_id = log['behavior']['movie_id']
                buys.append((user_id, movie_id, 0, timestamp))

        # print 'score: ', scores
        # print 'buys: ', buys
        model.insert_behaviors(buys)
        for s in scores:
            model.update_user_behavior(s[0], s[1], s[2])

