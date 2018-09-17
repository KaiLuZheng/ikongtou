#!/usr/bin/python3
#-*- encoding: utf8 -*-



import web
from sqlManager import iktSqlManager, configfile_defult

import configparser
import json


urls = ( 
    '/', 'index',
    '/api/dayorder', 'dayorder'
)


render = web.template.render('templates/')

class index:
    def GET(self):
        return render.index_test()

class dayorder:
    def GET(self):
        # check 
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






