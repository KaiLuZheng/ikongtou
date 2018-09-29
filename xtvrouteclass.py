#!/usr/bin/python3

import re
import time 
import sys

import json

import urllib
import urllib.request
import logging

test_url = 'http://www.zhiboo.net/001.htm'

charsets = ['utf8', 'gb2312']

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Host': 'www.zhiboo.net',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/69.0.3497.81 Chrome/69.0.3497.81 Safari/537.36',
}


def skipErrorCode(strings, code = 'gb2312'):
    shtml = ''

    for i in range(0, len(strings)-1):
        try:
            shtml = shtml + strings[i:i+1].decode(code)
        except Exception as e:
            print('skipErrorCode: %s'%e)
            continue
    return shtml



class reqCore():
    def __init__(self, url):
        self.url = url
        self.sourceInit()
        self.s2string()
        # self.html ok


    def sourceInit(self):
        req = urllib.request.Request(self.url, headers = headers)

        try:
            res = urllib.request.urlopen(req, timeout = 5.0)
        except Exception as e:
            raise Exception('init.error: %s'%e)

        self.res = res
        self.bhtml = res.read()

    
    def s2string(self):
        try:
            self.html = self.bhtml.decode(self.checkcode())
        except Exception as e:
            logging.error(e)
            self.resetpage()


    def checkcode(self):
        isString = False
        for i in charsets:
            try:
                shtml = self.bhtml.decode(i)
                isString = True
                self.charcode = i
                logging.debug('checkcode.ok: %s'%i)
                return i
            except Exception as e:
                logging.error('checkcode.error: %s'%e)
        raise Exception('checkcode error, need augment charset in %s:%s:%s'%(__file__,self.url,self.res.info()))


    def resetpage(self):
        # chardet , but now I do not want to use it now
        code = 'gb2312'        
        shtml = ''

        for i in range(0, len(self.bhtml)-1):
            try:
                shtml = shtml + self.bhtml[i:i+1].decode(code)
            except Exception as e:
                logging.error('reset page error: %s'%e)
                continue

        self.html = shtml
        



class xroute1(reqCore):
    infos = {}

    def __init__(self, url):
        super().__init__(url = url)

    def routeurl(self):
        iframeline = re.search(r'<iframe.*?/iframe>', self.html)

        try:
            logging.debug('%s: %s'%(self.url, iframeline.group()))
        except Exception as e:
            print(iframeline)
            with open('errorrequest.error', 'a') as f:
                f.write(self.html)
            raise e

        tvurlphp = re.search(r'src="(.*?)"', iframeline.group()).group(1)
        logging.debug('pick: %s'%tvurlphp)

        req = urllib.request.Request(tvurlphp)
        res = urllib.request.urlopen(req, timeout = 10.0)
        bhtml = res.read()


        try:
            phpstv = bhtml.decode('utf8')
        except Exception as e:
            logging.error(e)

        try:
            phpstv = bhtml.decode('gb2312')
        except Exception as e:
            logging.error(e)
            logging.error('char set error: use skip:%s'%self.url)
            phpstv = skipErrorCode(bhtml)


        tvroutejson = re.search(r'"https://.*?"', phpstv).group()[1:-1]

        req = urllib.request.Request(tvroutejson)
        res = urllib.request.urlopen(req)

        sjson = json.loads(res.read())['body']

        self.infos['contName'] = sjson['content']['contName']
        self.infos['contId'] = sjson['content']['contId']
        self.infos['playName'] = sjson['playBill']['playName']
        self.infos['realroute'] = sjson['urlInfo']['url']

        return json.dumps(self.infos)



if __name__ == '__main__':
    idnum = '5484'
    with open('tvmap.js', 'r') as f:
        sjson = json.loads(f.read())

    tv_url = sjson[idnum]['href']

    a = xroute1(url = tv_url)
    print(a.routeurl())














