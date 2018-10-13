#!/usr/bin/python3
#-*- encoding: utf8 -*-



import web
from sqlManager import iktSqlManager, configfile_defult
from translate import baiduTranslator as bdt

import configparser
import json
from urls import urls

from xtvrouteclass import xroute1

render = web.template.render('templates/')


tvmap = 'tvmap.js'


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


class tvshow:
    def GET(self, tvid):

        print(tvid)
        data = {}

        if tvid == 'test' :
            data['id'] = 0
            data['route'] = 'test'
            return render.tvshow(data)
        elif tvid in cctvid: 
            data['id'] = 1
            data['route'] = cctvmap[tvid]
            return render.tvshow(data)
        

        with open(tvmap, 'r') as f:
            sjson = json.loads(f.read())

        tv_url = sjson[tvid]['href']

        print(tv_url)

        try:
            a = xroute1(url = tv_url) 
            realroute = json.loads(a.routeurl())['realroute']

            data['id'] = 2
            data['route'] = realroute
            return render.tvshow(data)
        except Exception as e:
            return e



class image:
    def GET(self, img):
       with open('templates/img/'+img, 'rb') as f:
            return f.read()

class _videos:
    def GET(self, videos):
        with open('templates/videos/' + videos, 'rb') as f:
            return f.read()

class _jsons:
    def GET(self, jsons):
        with open('templates/js/' + jsons, 'rb') as f:
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
    app.run()






