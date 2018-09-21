#!/usr/bin/python3 
#-*- coding: utf8 -*- 


import pymysql
import configparser

import logging
import sys

import time



configfile_defult = 'conf.ini'

CHOSSE_DB = 'use %s;'
SELECT_TABLE = 'select %s from %s' 

INSERT_TABLE = 'insert into %s(%s) values(%s)' # tablename feilds values
DELETE_DATA = 'delete from %s %s' # tablename condition

class sqlOprateCore:
    def __init__(self, configfile = configfile_defult):
        # configfile should not be ''

        conf = configparser.ConfigParser()
        conf.read(configfile)
        self.conf = conf

    def connectSQL(self, host = '', user = '', password = ''):
        if user == '' or password == '' or host == '':
            try:
                self.user = self.conf.get('mysql','user')
                self.password = self.conf.get('mysql','password')
                self.host = self.conf.get('mysql', 'host')
            except Exception as e:
                logging.error(e)
                self.user = ''
                self.password = ''
                self.host = ''
                
            #print('%s:%s:%s'%(self.host,self.user,self.password))

            self.db = pymysql.connect(self.host, self.user, self.password)
            logging.debug( 'user: %s connected!' % self.user )
        else:
            self.user = user
            self.password = password
            self.host = host
            self.db = pymysql.connect(host, user, password)
        return self.db 

    def initorderline(self):
        self.cursor = self.db.cursor()
        return self.cursor

    def choosedb(self, dbname = ''):
        return self.orderdb( CHOSSE_DB % dbname )

    def selectTable(self, column = '*', tablename = ''):
        return self.orderdb( SELECT_TABLE % (column, tablename))

    def insertDate(self, tablename = '', fieldline = '', values = ''):
        #print(INSERT_TABLE % (tablename, fieldline, values))
        return self.orderdb( INSERT_TABLE % (tablename, fieldline, values) )

    def deleteDate(self, tablename, orderline):
        return self.orderdb( DELETE_DATA % (tablename, orderline) )

    def feedbackall(self):
        return self.cursor.fetchall()

    def orderdb(self, orderline = ''):
        if orderline == '':
            return False

        try:
            self.cursor.execute(orderline)
            self.db.commit()
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



class iktSqlManager(sqlOprateCore):
    # just to search and insert

    test_values = '"1", "1000-01-01 00:00:00", "3", "6", "5", "123456"'

    delete_id = 'where id = %d'
    dayorderinfos = 'dayorderinfo'
    def __init__(self):
        super().__init__('conf.ini')
        conf = self.conf

        self.dayorderfield = ''
        for i in conf.items('dayorderfield'):
            self.dayorderfield = self.dayorderfield + i[1] + ' '
        self.dayorderfield = self.dayorderfield.strip(' ').replace(' ', ', ')
        #print(self.dayorderfield)
    
            
    def insert_dayorderinfo(self, values):
        return self.insertDate(self.dayorderinfos, self.dayorderfield, values = values)
        
    def check_dayorderinfo(self):
        return self.selectTable(tablename = self.dayorderinfos)
        

    def readnew_dayorderinfo(self, numbers = 5):
        infos = self.check_dayorderinfo()
        try:
            needinfo = infos[len(infos)-numbers:]
        except Exception as e:
            logging.error(e)
            return None 
        
        return needinfo





if __name__ == '__main__':
    try:
        debugflag = sys.argv[1] == 'debug'
    except:
        debugflag = False

    if debugflag:
        logging.basicConfig(level = logging.DEBUG)
    else:
        logging.basicConfig(level = logging.ERROR)
        a = iktSqlManager()
        a.connectSQL()


    a.initorderline()
    print("choose db: ", a.choosedb('ikongtoudb'))
#    print('check table: ', a.check_dayorderinfo())
#    print(a.insert_dayorderinfo(values = a.test_values))
#    print(a.deleteDate(tablename = 'dayorderinfos', orderline = a.delete_id%5))
    print('check table: ', a.check_dayorderinfo())
    #print(a.readnew_dayorderinfo(1))

    a.closeSQL()
