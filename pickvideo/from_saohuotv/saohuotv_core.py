#!/usr/bin/python3


import urllib
import urllib.request
import re

from baseTool_saohuotv import staticResponse_post
from baseTool_saohuotv import staticResponse
from baseTool_saohuotv import bytes2strings
from baseTool_saohuotv import saveAsHtml

import sys
import logging
import time
import json

host_url = 'http://v.saohuotv.com'
search_url = 'http://v.saohuotv.com/search.php'
search_key = 'searchword'
searchvalue = '武动乾坤'


headers = {}
headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/69.0.3497.81 Chrome/69.0.3497.81 Safari/537.36'

def searchInfos(search_value = searchvalue):
    post_data = {search_key : search_value}
    
    try:
        res = staticResponse_post(search_url, headers = headers, data = post_data)
    except Exception as e:
        logging.error('post.error %s'%e)
        raise Exception('post.error')

    bhtml = res.read()
    shtml = bytes2strings(bhtml)

    vlist = re.search(r'<ul class="v_list".*?</ul>', shtml).group()
    vcontents = re.findall(r'<li>.*?</li>', vlist)


    infos = []
    for i in vcontents:
        info = {}
        info['href'] = host_url + re.search(r'href="(.*?)"' , i).group(1)
        info['title'] = re.search(r'title="(.*?)"', i).group(1)
        info['note'] = re.search(r'v_note">(.*?)<', i).group(1)
        infos.append(info)

        '''
        for j in info:
            print('%s:%s'%(j, info[j]))
        '''
    logging.debug(infos)
    return json.dumps(infos)



video_url = 'http://v.saohuotv.com/play/28928-0-0.html'
video_url = 'http://v.saohuotv.com/play/6365-1-0.html'
video_url = 'http://v.saohuotv.com/play/6365-0-0.html'
def xVideoRoute(url):
    logging.debug(url)
    res = staticResponse(url, headers = headers)
    bhtml = res.read()
    shtml = bytes2strings(bhtml)

    vframe = re.search(r'<iframe.*?/iframe>', shtml, re.S).group()
    vSrc = re.search(r'src="(.*?)"', vframe).group(1)

    print(vSrc)
    time.sleep(0.5)

    res = staticResponse(vSrc, headers = headers)
    bhtml = res.read()
    shtml = bytes2strings(bhtml)

    post_line = re.search(r'post\(".*?}', shtml).group()
    logging.debug(post_line)

    route = 'error'
    try:
        route = re.search(r'"http.*?"', post_line).group()[1:-1]
    except Exception as e:
        logging.error('pick route.error: %s'%e)
    else:
        logging.debug(route)
        return route
        
    # if http failed
    # http://play.hhplayer.com/myplay/url.php ### post
    search_php = 'http://play.hhplayer.com/myplay/url.php'
    try:
        route = re.search(r'{.*?}', post_line).group()
    except Exception as e:
        logging.error('pick {}.error: %s'%e)
        return route

    if re.search(r'Md5', route) :
        route = route.replace(r"sign($('#hdMd5').val())", '"ab59fe38d48ab5d6761fdd3e2a7aloij"')
        # ab59 loij
        search_php = 'http://play.hhplayer.com/mdparse/url.php'

    route = eval(route)

    res = staticResponse_post(search_php, headers = headers, data=route)
    time.sleep(0.5)
    sjson = json.loads(res.read())
    logging.debug(sjson)
    route = sjson['url']
    logging.debug(route)

    return route





test_url = 'http://v.saohuotv.com/movie/39358.html'
test_url = 'http://v.saohuotv.com/movie/39746.html'
def xVideolist(url):
    res = staticResponse(url, headers = headers)
    bhtml = res.read()
    shtml = bytes2strings(bhtml)
    saveAsHtml(shtml, 'tmp.html')

    '''
    with open('tmp.html', 'r') as f:
        shtml = f.read()

    '''
    isPicked = False
    vlist = ''
    try:
        vlist = re.search(r'<ul class="play_list".*?</ul>', shtml, re.S).group()
        isPicked = True
    except Exception as e:
        logging.error('play_list.error: %s'%e)

    if isPicked is False:
        vlist = re.search(r'<ul class="large_list".*?</ul>', shtml, re.S).group()

    vlist = re.findall(r'<a.*?/a>', vlist)

    playlist = []
    for i in vlist:
        playport = {}
        playport['href'] = host_url + re.search(r"href='(.*?)'", i).group(1) # href
        playport['note'] = '第' + re.search(r'>(.*?)<', i).group(1) + '集' # number
        playlist.append(playport)

    if len(playlist) == 1:
        playlist[0]['note'] = playlist[0]['note'][1:-1]

    for i in playlist:
        logging.debug(i)

    return json.dumps(playlist)



if __name__ == '__main__':
    logging.basicConfig(level = logging.DEBUG)

    #print(searchInfos())
    #xVideolist(test_url)
    xVideoRoute(video_url)



