#!/usr/bin/python3
#-*- encoding: utf8 -*-



_dir = (os.path.dirname(os.path.realpath(__file__)))
core_dir = main_dir + '/ispider/core'


import web

urls = ( '/', 'index'
)

class index:
    def GET(self):
        return 'hello world!'

#app = web.application(urls, globals())
app = web.application(urls, locals())

if __name__ == '__main__':
    app.run()






