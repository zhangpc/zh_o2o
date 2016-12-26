# -*- coding:utf-8 -*-
#!/usr/bin/python
from flask import Flask
import pymysql
from flask.ext.sqlalchemy import SQLAlchemy
from Fangfull.mondel.m_Message_res import Message_res
from config.Config import Flask_Config
app = Flask(__name__)
FlaskConfig = Flask_Config(app)
app = FlaskConfig.app
db = Flask_Config.get_db()

class Message_data(db.Model):
    __tablename__='message_data'
    data_id = db.Column(db.Integer,primary_key = True)
    data_name = db.Column(db.String(150))
    data_value = db.Column(db.String(100))
    data_describe = db.Column(db.String(150))
    res_id =  db.Column(db.Integer,db.ForeignKey(Message_res.res_id))
    def __init__(self ,data_id=None,data_name=None,data_value=None,data_describe=None):
        self.data_id = data_id
        self.data_name = data_name
        self.data_value = data_value
        self.data_describe = data_describe
    def __repr__(self):
        return '(%d,%s,%s,%s,%d)' % (self.data_id,self.data_name,self.data_value,self.data_describe,self.res_id)
if __name__ == "__main__":
    db.create_all()