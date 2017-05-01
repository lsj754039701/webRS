# -*- coding=utf-8 -*

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
