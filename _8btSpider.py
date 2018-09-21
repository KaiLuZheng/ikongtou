#!/usr/bin/env python3

from ispider import iSpider

import logging
import time

import configparser

import urllib
import urllib.request

import json
import random
import re
import sys

from sqlManager import iktSqlManager



'''
dayorderLabels = [  'title',
                    'post_date_format',
                    'desc',
                    'images',
]
'''

def buildparseline(char, number):
    parse = ''
    for i in range(0, number):
        parse = parse + char
    return parse

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
        获得日排名 json
        '''
        res = urllib.request.urlopen(self.day_order_url) 
        jsonlist = res.read().decode('utf8')
        sjson = json.loads(jsonlist)
#        logging.debug(sjson['list'][0]) # 查看格式
        return sjson

    def parse_xdayorder(self, sjson):
        '''
        截取需要的内容，并上传
        '''
        logging.info(sjson)

        conf = configparser.ConfigParser()
        conf.read('conf.ini')

        dayorderLabels = []
        for i in conf.items('dayorderlabels'):
            dayorderLabels.append(i[1])

        '''
        print(dayorderLabels)
        sys.exit()
        '''


        # temp deal 
        values = []
        #print(sjson)
        for i in dayorderLabels:
            info = sjson[i].replace('\r','').replace('\n', '') if type(sjson[i]) == str else sjson[i]
            if type(info) == list:
                for j in info:
                    values.append(j)
            elif type(info) == str:
                values.append(info)
            elif type(info) == int:
                values.append(str(info))
            else:
                e = '_8btspider.parse_xdayorder: data error ???'
                logging.error(e)
                raise Exception(e)
                
               
        #'"1", "1000-01-01 00:00:00", "3", "6", "5"' 
        # should be ensure the string not contain the ' ' '
        parse = ''
        for i in values:
            parse = parse + '"%s",'%i
        #print(parse)
       
        # update on mysql
        dbManager = iktSqlManager()
        dbManager.connectSQL()
        dbManager.initorderline()
        dbManager.choosedb('ikongtoudb')
        #print(dbManager.orderdb('show create table dayorderinfo;'))
        dbManager.insert_dayorderinfo(values = str(parse.strip(',')))

        '''
        可能会出现编码的问题，这与数据库默认的编码设置有关，需要实现统一
        '''



if __name__ == '__main__':

    logging.basicConfig( level = logging.INFO, 
                        filename = time.strftime('%Y%m',time.localtime()) + '.log',
                        filemode = 'a',
                        format = '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
    )
#    logger.info(time.strftime('%Y%m',time.localtime()) + '.txt')

    while True:
        logging.info('crap 8btc.')

        a = _8btSpider()
        a.start()
        a.join()

        logging.info('ok.')

        time.sleep(86400)




