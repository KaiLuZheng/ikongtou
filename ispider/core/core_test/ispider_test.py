#!/usr/bin/env python3

#creater: Kailu Zheng



import logging
import threading

import time


# can be controled by a file
logging.basicConfig(level = logging.DEBUG,
                    #format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)




class iSpider(threading.Thread):
    urls=[]
    def __init__(self, out, func,sec):
        threading.Thread.__init__(self)
        logging.debug('I am iSpider')

        self.out = out
        self.func = func
        self.sec = sec

    def run(self):
        self.func(self.out, self.sec) 
        pass

     

class test:
    def __init__(self):
        a = iSpider('test thread call a', self.logg, 1)
        b = iSpider('test thread call b', self.logg, 3)

        a.start()
        b.start()

        while True:
            time.sleep(2.5)
            logging.debug('main test')

    def logg(self, a, sec):
        while True:
            logging.debug(a)
            time.sleep(sec)



# test
class baiduSpider(iSpider):
    urls = [
            'https://www.baidu.com'
]
    def __init__(self):
        super().__init__()
        logging.debug('I am baiduSpider')
        logging.debug(self.urls)

        



if __name__ == '__main__':
    A = test()
    #B = baiduSpider()





