#!/usr/bin/python3
#-*- encoding: utf8 -*-



import web


urls = ( 
    '/', 'index'
)


render = web.template.render('templates/')

class index:
    def GET(self):
        return render.index_test()


app = web.application(urls, locals())
#app = web.application(urls, globals())


if __name__ == '__main__':
    app.run()






