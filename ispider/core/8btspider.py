#!/usr/bin/env python3

from ispider import iSpider

import logging
import time

logging.basicConfig(level = logging.DEBUG,

)

import urllib
import urllib.request
from urllib import parse

import json
import random
import re

class _8btSpider(iSpider):

    host_url = 'https://www.8btc.com'
    day_orderby_api = 'https://app.blockmeta.com/w1/news/list?'
    param = {   'post_type':'post',
                'num':5,
                'orderby':'day'
    }

    def __init__(self):
        super().__init__()
        logging.debug('I am 8bt spider')
        
        self.day_order_url = self.day_orderby_api+parse.urlencode(self.param)


    def run(self):
        resjson = self.reqdayorder()
        logging.debug(resjson)

    def reqdayorder(self):
        res = urllib.request.urlopen(self.day_order_url) 
        jsonlist = res.read().decode('utf8')
        return json.loads(jsonlist)
        

    def parse(self):
        pass



if __name__ == '__main__':
    a = _8btSpider()
    a.start()

    a.join()




