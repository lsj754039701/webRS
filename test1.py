import multiprocessing

d = 0

def fun1():
    global d
    d += 1
    print d

def fun2():
    global d
    d -= 1
    print d

if __name__ == "__main__":
    pass
