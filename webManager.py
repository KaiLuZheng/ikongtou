#!/usr/bin/python3
#-*- encoding: utf8 -*-



import web
from sqlManager import iktSqlManager, configfile_defult
from translate import baiduTranslator as bdt

import configparser
import json
from urls import urls
import logging

### 

import sys, os
maindir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(maindir + '/picktvshow')
sys.path.append(maindir + '/pickvideo/from_saohuotv')
from zhibooStream_api import xroute_tvmap as zhiboo_xroute
from haoquStream_api import xroute_tvmap as haoqu_xroute

from saohuotv_core import searchInfos as saohuosearch
from saohuotv_core import xVideoRoute as saohuovideo
from saohuotv_core import xVideolist as saohuo_videolist

###


render = web.template.render('templates/')


cctvid = ['055', '061', '056', '085', '003', '057', '086', '058']
cctvmap = {'055':'cctv2', 
    '056':'cctv3', 
    '085':'cctv4', 
    '003':'cctv5', 
    '057':'cctv6', 
    '086':'cctv7', 
    '058':'cctv8', 
    '061':'cctv10',
 }

class tvindex:
    def GET(self):
        pass

class xhaoquIframe:
    def GET(self):
        pass

    def POST(self, data):

        return 'hello'


class saohuo_video:
    def GET(self):       
        data = ''
        try:
            data = web.input().url
            print(data)
        except Exception as e:
            print(e)
        else:
            routelist = saohuo_videolist(data)

        return routelist


class saohuo_search:
    def GET(self):
        data = ''
        try:
            data = web.input().searchword
            print(data)
        except Exception as e:
            print(e)
        else:
            infos = saohuosearch(data)

        if data == '':
            return render.saohuotv_search()
        else:
            return infos


class saohuo_play:
    def GET(self):
        data = ''
        try:
            data = web.input().url
            print(data)
        except Exception as e:
            print('error: ', e)
        else:
            try:
                route = saohuovideo(data)
                print('webmanager: ', route)
            except Exception as e:
                print('error: %s'%e)
                return '<a href="' + data +'"><h2><strong>Jump to look</strong></h2><a>'

        if data == '' or route == 'error':
            return '<a href="' + data +'"><h2><strong>Jump to look</strong></h2><a>'

        return render.saohuotv(route)
        

class jump_haoqu:
    def GET(self):
        data = web.input().id
        print(data)

        return render.jumphaoqu('http://localhost:8080/haoqutv/' + data)
        #return render.jumphaoqu('http://www.lumeno.club/haoqutv/' + data)


class haoqu_tvshow:
    def GET(self, tvid):
        print(tvid)
        try:
            data = haoqu_xroute(tvid)
        except Exception as e:
            return ('%s: no signal'%e)

        print(data['sourdid'])

        return render.tvshow_haoqu(data)


class zhiboo_tvshow:
    def GET(self, tvid):

        print(tvid)
        data = zhiboo_xroute(tvid)
        print(data)
       
        if data['sourid'][1] == '':
            return data['tvname'] + ':no signal'

        return render.tvshow(data)



class image:
    def GET(self, img):
       with open('templates/img/'+img, 'rb') as f:
            return f.read()

class _videos:
    def GET(self, videos):
        with open('templates/videos/' + videos, 'rb') as f:
            return f.read()

class cks:
    def GET(self, jsons):
        with open('templates/ckplayer/' + jsons, 'rb') as f:
            return f.read()


class translate:
    def GET(self):
        word = web.input().word
        try:
            data = bdt().translateWord(word)
            data['code']  = 0
        except:
            data = {'error':'input error', 'code': -1}
        return json.dumps(data)


    def POST(self):
        param = json.loads(web.data().decode('utf8'))
        word = param['word']
        data = bdt().translateWord(word)
        return json.dumps(data)


class index:
    def GET(self):
        dbManager = iktSqlManager()
        dbManager.connectSQL()
        dbManager.initorderline()
        dbManager.choosedb('ikongtoudb')
        data = dbManager.readnew_dayorderinfo()
        dbManager.closeSQL()

        conf = configparser.ConfigParser()
        conf.read(configfile_defult)
        infolabels = []
        for i in conf.items('dayorderfield'):
            infolabels.append(i[1])

        #print(infolabels)

        infos = []
        for j in data: 
            tmpdata = {}
            for num, i in enumerate(j[1:]):
                tmpdata[infolabels[num]] = j[1+num]
            tmpdata['dayformat'] = tmpdata['dayformat'].strftime('%Y-%m-%d %H:%M:%S')
            infos.append(tmpdata)

        return render.index_test(infos)


class dayorder:
    def GET(self):
        # check 
        web.header('content-type','text/json')

        number = int(web.input().query)

        dbManager = iktSqlManager()
        dbManager.connectSQL()
        dbManager.initorderline()
        dbManager.choosedb('ikongtoudb')
        data = dbManager.readnew_dayorderinfo(number)
        dbManager.closeSQL()

        conf = configparser.ConfigParser()
        conf.read(configfile_defult)
        infolabels = []
        for i in conf.items('dayorderfield'):
            infolabels.append(i[1])

        #print(infolabels)

        infos = []
        for j in data: 
            tmpdata = {}
            for num, i in enumerate(j[1:]):
                tmpdata[infolabels[num]] = j[1+num]
            tmpdata['dayformat'] = tmpdata['dayformat'].strftime('%Y-%m-%d %H:%M:%S')
            infos.append(tmpdata)

        return json.dumps(infos)



app = web.application(urls, locals())
#app = web.application(urls, globals())


if __name__ == '__main__':
    logging.basicConfig(level = logging.DEBUG)
    app.run()





