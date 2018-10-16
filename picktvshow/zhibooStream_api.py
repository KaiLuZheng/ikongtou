#!/usr/bin/python3

# zhibooStream_api

import json

import time
import re
import logging

from baseTool import staticResponse
from baseTool import bytes2strings


#{'cctv4': 
test_item = {
    #'tv_page_href': "http://www.zhiboo.net/./047.htm",
    #'tv_page_href': "http://www.zhiboo.net/./783.htm",
    #'tv_page_href': "http://www.zhiboo.net/./015.htm",
    'tv_page_href': "http://www.zhiboo.net/./1970.htm",
    'tvname': "CCTV1" 
}
test_url = test_item['tv_page_href']


# crap tvmap
def gainIframeSrc(url):
    res = staticResponse(url)
    shtml = bytes2strings(res.read())
    shtml = shtml.replace('\r\n', '').replace('\n\r', '')
   
    mode = ''
    try:     
        iframeline = re.search(r'<p><iframe (.*?)</p>', shtml, re.S).group()
        iframeSrc = re.search(r'src="(.*?)"', iframeline, re.S).group(1)
        mode = 'iframe'
        return (mode, iframeSrc)
    except Exception as e:
        logging.error('[%s] gain iframe.error: %s'%(url, e))

    try:
        embedline = re.search(r'<embed(.*?)>', shtml, re.S).group()
        mode = 'embed'
    except Exception as e:
        logging.error('[%s] gain embed.error: %s'%(url, e))
    else:
        try:
            flashvar = re.search(r'flashvars="(.*?)"', embedline).group(1)
        except Exception as e:
            logging.error('[%s] gain embed, flashvar.error: %s'%(url, e))
        else:
            try:
                stream = re.search(r'a=(.*?)&', flashvar).group(1)
                stream = stream.replace('%3A', ':').replace('%2F', '/')
                return (mode, stream)
            except Exception as e:
                logging.error('[%s] gain embed, flashvars, a.error: %s'%(url, e))

            try: 
                stream = re.search(r'file=(.*?)&', flashvar).group(1)
                return (mode, stream)
            except Exception as e:
                logging.error('[%s] gain embed, flashvars, file.error: %s'%(url, e))     
                return (mode, '')

        try:
            srcbody = re.search(r'src="(.*?)"', embedline).group(1)
            stream = re.search(r'url=(.*?)&', srcbody).group(1)
            return (mode, stream)
        except Exception as e:
            logging.error('[%s] gain embed, src.error: %s'%(url, e))    

    try:
        flashvars = re.search(r'flashvars=(.*?);', shtml, re.S).group()
        stream = re.search(r'f:\'(.*?)\'', flashvars).group(1)
        mode = 'flashvars'
        return (mode, stream)
    except Exception as e:
        logging.error('[%s] gain flashvar.error: %s'%(url, e))
        return (mode, '')



# replace sourdid by route
def streamRoute_zhiboo(tvmap):
    # request extend_url
    if tvmap['sourid'] == ['','']:
        return tvmap
    
    if tvmap['sourid'][0] == 'iframe':
        pass
    else:
        return tvmap

    # iframe url
    url = tvmap['sourid'][1]
    res = staticResponse(url)  
    shtml = bytes2strings(res.read())

    getline = re.search(r'xmlhttp.open(.*?);', shtml).group()
    routeurl = re.search(r'"https://.*?"', getline).group()[1:-1]

    res = staticResponse(routeurl)
    bhtml = res.read()
    sjson = json.loads(bhtml)['body']

    route = sjson['urlInfo']['url']
    tvmap['sourid'][1] = route.replace("http://h5live.gslb.cmvideo.cn","http://mgzb.live.miguvideo.com:8088")

    return tvmap

# pick tvmap from file
def picktvmap(pagecode, filename):
    with open(filename, 'r') as f:
        sjson = json.loads(f.read())
    return sjson['tvmap'][pagecode]


# manager function
import os
mydir = os.path.dirname(os.path.realpath(__file__))
def xroute_tvmap(pagecode, filename = mydir + '/tvmap/zhiboo.js'):
    tvmap = picktvmap(pagecode, filename = filename)
    res = streamRoute_zhiboo(tvmap)
    return tvmap


if __name__ == '__main__':
    logging.basicConfig(level = logging.DEBUG)

    pagecode = '001' 
    print(xroute_tvmap(pagecode))

    '''
    # crap tv map
    item = gainIframeSrc(test_url)
    print('%s : %s'%(item[0], item[1]))
    '''

