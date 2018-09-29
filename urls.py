#!/usr/bin/python3
#-*- coding: utf8 -*-

urls = (
    '/', 'index',
    '/api/dayorder', 'dayorder',
    '/api/translate', 'translate',
    '/tvindex/', 'tvindex',
    '/tv/(.*)', 'tvshow',
    '/img/(.*)', 'image',
    '/js/(.*)', '_jsons',
    '/videos/(.*)', '_videos',
)


    




