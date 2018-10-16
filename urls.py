#!/usr/bin/python3
#-*- coding: utf8 -*-

urls = (
    '/', 'index',
    '/api/dayorder', 'dayorder',
    '/api/translate', 'translate',
    '/api/xhaoquIframe', 'xhaoquIframe',
    '/tvindex/', 'tvindex',
    '/zhibootv/(.*)', 'zhiboo_tvshow',
    '/haoqutv/(.*)', 'haoqu_tvshow',
    '/jump/haoqu', 'jump_haoqu',
    '/img/(.*)', 'image',
    '/ckplayer/(.*)', 'cks',
    '/videos/(.*)', '_videos',
)


    




