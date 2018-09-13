#!/usr/bin/python3 
#-*- coding: utf8 -*- 


import pymysql
import configparser

import logging
import sys

import time

try:
    debugflag = sys.argv[1] == 'debug'
except:
    debugflag = False

if debugflag:
    logging.basicConfig(levle = logging.DEBUG)
else:
    logging.basicConfig(level = logging.ERROR)


CHOSSE_DB = 'use %s;'
SELECT_TABLE = 'select %s from %s'

class sqlOprateCore:
    def __init__(self, configfile = 'conf.ini'):
        # configfile should not be ''

        conf = configparser.ConfigParser()
        conf.read(configfile)

        try:
            self.user = conf.get('mysql','user')
            self.password = conf.get('mysql','password')
        except Exception as e:
            logging.error(e)
            self.user = ''
            self.password = ''
        #print('%s:%s'%(self.user,self.password))
    
    def connectSQL(self, host = '', user = '', password = ''):
        if user == '' or password == '' or host == '':
            self.db = pymysql.connect('localhost', self.user, self.password)
        else:
            self.db = pymysql.connect('localhost', self.user, self.password)
        return self.db 

    def initorderline(self):
        self.cursor = self.db.cursor()
        return self.cursor

    def choosedb(self, dbname = ''):
        return self.orderdb( CHOSSE_DB % dbname )

    def selectTable(self, column = '*', tablename = ''):
        return self.orderdb( SELECT_TABLE % (column, tablename))


    def insertDate(self):
        pass

    def deleteDate(self):
        pass


    def feedbackall(self):
        return self.cursor.fetchall()

    def orderdb(self, orderline = ''):
        if orderline == '':
            return False

        try:
            self.cursor.execute(orderline)
            return self.feedbackall()
        except Exception as e:
            raise(e) 

    def closeSQL(self):
        self.db.close()


    def test(self):
        db = self.db
        cursor = db.cursor() # 游标对象
        cursor.execute('show tables;')
        data = cursor.fetchone() # 获得数据
        print (len(data))



class sqlManager(sqlOprateCore):
    def __init__(self):
        super().__init__('conf.ini')





if __name__ == '__main__':
    a = sqlManager()
    a.connectSQL()
    a.initorderline()
    print(a.choosedb('ikongtoudb'))
    print(a.selectTable(tablename = 'dayorderinfos'))
    a.closeSQL()
