from queue import Queue

from threading import Thread
#线程事件函数


def parse_html():
    print('来玩呀小哥哥')


def thinel():
    for i in range(5):
        t=Thread(target=parse_html)
        t.start()
        

T=Thread(target=thinel)
T.start()
T.join()