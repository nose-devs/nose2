from multiprocessing import Process


def method2():
    return


def method():
    p = Process(target=method2)
    p.start()
    p.join()
    return True
