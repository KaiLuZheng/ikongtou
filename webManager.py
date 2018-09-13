#!/usr/bin/python3
#-*- encoding: utf8 -*-



import web

urls = ( '/', 'index'
)



class index:
    def GET(self):


        return open('index_test.html', 'r').read()




#app = web.application(urls, globals())
app = web.application(urls, locals())

if __name__ == '__main__':
    app.run()






