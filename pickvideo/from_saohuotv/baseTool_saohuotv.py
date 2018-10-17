#!/usr/bin/python3



import re
import urllib
import urllib.request
import urllib.parse

import logging

codelist = ('utf8', 'gbk', 'gb2312')

def _pickName_H5(string):
    string2 = re.search(r'/(.*?)$', string) 
    
    if string2 is None:
        return string
    else:
        return _pickName_H5(string2.group()[1:])


def saveAsHtml(filebody, filename):
    with open(filename, 'w') as f:
        f.write(filebody)


def skipErrorCode(strings):
    shtml = ''
    for i in range(0, len(strings)-1):
        try:
            shtml = shtml + strings[i:i+1].decode('utf8')
        except Exception as e:
            continue
    return shtml


def bytes2strings(bytesItem):
    isTrans = False
    for i in codelist:
        try:
            strings = bytesItem.decode(i)
            isTrans = True
            logging.debug('transCode is %s'%i)
            return strings
        except Exception as e:
            logging.error('transCode %s.error: %s'%(i, e))

    if isTrans is False:
        logging.info('code error: skip code... ')
        return skipErrorCode(bytesItem)


def staticResponse(url, headers = {}, timeout = -1):
    req = urllib.request.Request(url, headers = headers)
    if timeout == -1:
        res = urllib.request.urlopen(req)
    else:
        res = urllib.request.urlopen(req, timeout = timeout)
    return res
        

def staticResponse_post(url, headers = {}, data={}, timeout = -1):
    req = urllib.request.Request(url, headers = headers, data=urllib.parse.urlencode(data).encode('utf8'))
    if timeout == -1:
        res = urllib.request.urlopen(req)
    else:
        res = urllib.request.urlopen(req, timeout = timeout)
    return res
 

