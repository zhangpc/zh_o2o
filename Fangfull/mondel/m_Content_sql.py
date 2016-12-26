# -*- coding:utf-8 -*-
#!/usr/bin/python
from flask import Flask
import pymysql
from flask.ext.sqlalchemy import SQLAlchemy

from config.Config import Flask_Config
app = Flask(__name__)
FlaskConfig = Flask_Config(app)
app = FlaskConfig.app
db = Flask_Config.get_db()

class Content_sql(db.Model):
    __tablename__='content_sql'

    sql_id = db.Column(db.Integer,primary_key = True)
    sql_name = db.Column(db.String(150))
    sql_host = db.Column(db.String(100))
    sql_port = db.Column(db.String(100))
    sql_user_name = db.Column(db.String(100))
    sql_user_passwd = db.Column(db.String(100))
    sql_db = db.Column(db.String(100))
    sql_type = db.Column(db.SmallInteger,default = 0)
    def __init__(self ,sql_name=None,sql_host=None,sql_port=None,sql_user_name=None,sql_user_passwd=None,sql_db=None,sql_type = None):
        self.sql_name = sql_name
        self.sql_host = sql_host
        self.sql_port = sql_port
        self.sql_user_name = sql_user_name
        self.sql_user_passwd = sql_user_passwd
        self.sql_db = sql_db
        self.sql_type = sql_type
    def __repr__(self):
        return '(%d,%s,%s,%s,%s,%s,%s,%d)' % (self.sql_id,self.sql_name, self.sql_host,self.sql_port,self.sql_user_name,self.sql_user_passwd,self.sql_db,self.sql_type)
        # return self.sql_id,self.sql_name,self.sql_type,self.sql_host,self.sql_port,self.sql_user_name,self.sql_user_passwd,self.sql_db

if __name__ == "__main__":
    db.create_all()