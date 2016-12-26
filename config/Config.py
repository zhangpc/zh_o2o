# -*- coding:utf-8 -*-
#!/usr/bin/python
from flask import Flask
import pymysql
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text, Column, Integer, String, Sequence

# IP = 'http://testwww.fangfull.com/'
# IP_fangfull = 'http://testwww.fangfull.com/'
# IP_admin = 'http://test2www.xqshijie.com/'
### ----------上面的暫時不確定是否有用

IP_Jigoujingjiren = 'agentjjrwap.php'
IP_Quanminjingjiren = 'qmjjrwap.php'
#
# IP_APP = 'https://103.10.86.28/'

class Ip():
    def set_Ipblue(self,ip):
        self.ipblue = ip

    def set_Ipred(self,ip):
        self.ipred = ip

    def get_Ipblue(self):
        return self.ipblue

    def get_Ipred(self):
        return self.ipred


class SqlConnect():
    def get_fangfull_test_sql(self):
        sql_connect = {}
        sql_connect['host'] = '103.10.86.28'
        sql_connect['port'] = '3306'
        sql_connect['user'] = 'test'
        sql_connect['passwd'] = 'mhxzkhl'
        sql_connect['db'] = 'test_zh_o2o_db'
        return sql_connect
    def get_xqsj_test_sql(self):
        sql_connect = {}
        sql_connect['host'] = '103.10.86.28'
        sql_connect['port'] = '3306'
        sql_connect['user'] = 'test'
        sql_connect['passwd'] = 'mhxzkhl'
        sql_connect['db'] = 'xqsj_db'
        return sql_connect

    def get_fangfull_beta_sql(self):
        sql_connect = {}
        sql_connect['host'] = '103.10.86.25'
        sql_connect['port'] = '3306'
        sql_connect['user'] = 'xqshijie_test'
        sql_connect['passwd'] = 'xqsj@#%test!@#'
        sql_connect['db'] = 'zh_o2o_db'
        return sql_connect

    def get_xqsj_bate_sql(self):
        sql_connect = {}
        sql_connect['host'] = '103.10.86.25'
        sql_connect['port'] = '3306'
        sql_connect['user'] = 'xqshijie_test'
        sql_connect['passwd'] = 'xqsj@#%test!@#'
        sql_connect['db'] = 'xqsj_db'
        return sql_connect

db = None
class Flask_Config():
    def __init__(self,app):
        self.app = app
        app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root:root@localhost/zhonghong_o2o'
        global db
        db = SQLAlchemy(self.app)
    @staticmethod
    def get_db():
        return db
    @staticmethod
    def text_sql(sqlstr):
        session = Flask_Config.get_db().session()
        sql = text(str(sqlstr))
        res = session.execute(sql).fetchall()
        session.close()
        return res
    @staticmethod
    def submit():
        db.session.commit()


if __name__ == '__main__':
    # print(IP_blue)
    ip = Ip()
    # ip.set_Ipblue('sdfsdf')

    print()