#!/usr/bin/env python3

#creater: Kailu Zheng



import logging
import threading

# can be controled by a file
logging.basicConfig(level = logging.DEBUG,
                    #format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class iSpider(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        logging.debug('I am iSpider')

    def run(self): # ex html for detail
        self.parse() 
        pass

    def parse(self): # individuation like detail
        pass
     


# test

import urllib
import urllib.request
import time

class baiduSpider(iSpider):
    def __init__(self, urlhost='https://www.baidu.com', headers=None):
        super().__init__()

        self.url = urlhost
        self.headers = headers
        logging.debug(self.url)
        
    def run(self):
        self.parse('asdf')

    def parse(self, name): # individuation 
        logging.debug(urllib.request.urlopen(self.url).read())
        logging.debug(name)
        

class spidermanager():
    def __init__(self):
        B = baiduSpider()
        B.start()

import json
import random
import re

if __name__ == '__main__':
    #manager = spidermanager() 
    #logging.debug(6438.673542714115 * 6.8726)

    while True:
        req = urllib.request.urlopen('https://api.schail.com/v3/ticker/summary?type=0&sort=1&offset=0&limit=100&top=0')
        coins = req.read().decode('utf8')

        BTC = json.loads(coins)['data']['summaryList'][0]['price']

        req = urllib.request.urlopen('http://m.cmbchina.com/Rate/FxRealrateDetail.aspx?name=%u7F8E%u5143')
        # %u7F8E%u5143 = 美元
        html = req.read().decode('utf8') 
        logging.debug(re.findall(r'<div class="box-flex-1 text-right">(.*?)</div>', html)[4])

        huilv = float(re.findall(r'<div class="box-flex-1 text-right">(.*?)</div>', html)[4])
        logging.debug(float(BTC)*huilv/100)


        time.sleep(random.uniform(5,9))









