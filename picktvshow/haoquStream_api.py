#!/usr/bin/python3

# haoquStream_api

import json

import time
import re
import logging

from baseTool import staticResponse
from baseTool import bytes2strings


#{'cctv4': 
test_item = {
    'href': "/1/cctv4.html",
    'tv_page_href_mobile': "http://m.haoqu.net/1/cctvysjp.html", 
    'tv_page_href_pc': "http://www.haoqu.net/1/cctvysjp.html",
    'tvname': "CCTV4",
}

# read a file of js wicth named 'player.js'
playerjsex = 'http://www.haoqu.net/e/extend/tv.php?id=' # + sourid

   
# gain sourid
# give a url

def gainSourid(url):
    logging.debug('x url: %s'%url)
    mode = re.search(r'//(.*?)\.', url).group(1)
    
    res = staticResponse(url)
    bhtml = res.read()
    shtml = bytes2strings(bhtml)
  
    try: 
        tab_syb = re.search(r'<div class="tab-syb"(.*?)</div>', shtml, re.S).group()
    except Exception as e:
        logging.error('gain sourdid %s.error: %s'%(mode,e))
        return False

    if mode == 'www':
        return re.findall(r'data-player="(.*?)"', tab_syb)
    elif mode == 'm':
        return re.findall(r'value="(.*?)"', tab_syb)


def sourdidPages(tvmap = test_item):
    urls = [tvmap['tv_page_href_mobile'], tvmap['tv_page_href_pc']]
    sourdid = []
    for i in urls:
        time.sleep(0.5)
        sourdline = gainSourid(i)
        if sourdline is not False:
            sourdid = sourdid + sourdline

    sourdid_pages = []
    for i in set(sourdid):
        sourdid_pages.append(playerjsex + i)
    tvmap['sourdid'] = sourdid_pages
    return tvmap


# ex the route from iframe 
def exiframe(url):
    res = staticResponse(url)
    shtml = bytes2strings(res.read())
   
    try: 
        evalline = re.search(r'eval(.*?)\}\)\)', shtml).group()
    except Exception as e:
        logging.error('eval gain failed.error: %s'%e)
    else:
        funcline = re.search(r'eval(.*)$', evalline).group(1)
        param = funcline[1:-1].split('p}')[1]
        return param
    return url
    '''
    # else not now
    try:
        pass
    except Exception as e:
        pass

    '''


# replace sourdid by route
def streamRoute_haoqu(tvmap):
    # request extend_url
    souridlist = tvmap['sourdid']
   
    if souridlist == []:
        return []

    routelist = []
    for i in souridlist:
        time.sleep(0.5)
        res = staticResponse(i)  
        shtml = bytes2strings(res.read())

        # pidk iframe body
        signal = re.search(r'signal = \'(.*?)\'', shtml, re.S).group(1)

        signal = signal.split('$')

        if signal[2] == 'iframe':
            signal[1] = exiframe(signal[1])        

        routelist.append(signal)

    tvmap['sourdid'] = routelist
    return tvmap


# pick tvmap from file
def picktvmap(pagecode, filename):
    with open(filename, 'r') as f:
        sjson = json.loads(f.read())
    return sjson['tvmap'][pagecode]


# manager function
import os
mydir = os.path.dirname(os.path.realpath(__file__))
def xroute_tvmap(pagecode, filename = mydir + '/tvmap/haoqu.js'):
    tvmap = picktvmap(pagecode, filename = filename)
    res = streamRoute_haoqu(tvmap)
    return res
    

if __name__ == '__main__':
    logging.basicConfig(level = logging.DEBUG)
    ''' 
    sourid = sourdidPages(test_item)
    print(sourid)
    '''

    pagecode = 'cctv6'
    print(xroute_tvmap(pagecode))

        #exiframe('http://p.18kf.net/tv_app_v2.php?from=mg&id=604267259')
    #exiframe('http://player.haoqu.net/00/567it/cctv3.html')
    #exiframe('http://player.haoqu.net/swf.html?id=http://g.alicdn.com/de/prismplayer-flash/1.2.16/PrismPlayer.swf?vurl=http://117.169.120.209:8080/live/cctv-3/.m3u8&autoPlay=true')
