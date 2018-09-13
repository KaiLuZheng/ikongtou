#!/usr/bin/env python3

from ispider import iSpider

import logging
import time

logging.basicConfig(level = logging.DEBUG,

)

import urllib
import urllib.request

import json
import random
import re


dayorderLabels = [  'title',
                    'post_date_format',
                    'desc',
                    'images',
]

class _8btSpider(iSpider):

    host_url = 'https://www.8btc.com'
    day_orderby_api = 'https://app.blockmeta.com/w1/news/list?'
    param = {   'post_type':'post',
                'num':5,
                'orderby':'day'
    }

    def __init__(self):
        super().__init__()
        
        self.day_order_url = self.day_orderby_api + urllib.parse.urlencode(self.param)

#   def run(self): # run parse        

    def parse(self):
        resjson = self.reqdayorder()
        for i in resjson['list']:
            self.parse_xdayorder(i)

    def reqdayorder(self):
        '''
        获得日排名json
        '''
        res = urllib.request.urlopen(self.day_order_url) 
        jsonlist = res.read().decode('utf8')
        sjson = json.loads(jsonlist)
#        logging.debug(sjson['list'][0]) # 查看格式
        return sjson

    def parse_xdayorder(self, sjson):
        '''
        获取需要的内容 
        '''
        infos = {}
        for i in dayorderLabels:
            infos[i] = sjson[i].replace('\r','').replace('\n', '') if type(sjson[i]) == str else sjson[i]
       
        # update on mysql
        for i in infos:
            print(type(infos[i]) == list)



if __name__ == '__main__':
    a = _8btSpider()

    a.start()

    a.join()




