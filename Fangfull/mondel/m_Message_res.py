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

class Message_res(db.Model):
    __tablename__='message_res'
    res_id = db.Column(db.Integer,primary_key = True)
    res_name = db.Column(db.String(150))
    res_describe = db.Column(db.String(150))
    def __init__(self ,res_id=None,res_name=None,res_describe= None):
        self.res_id = res_id
        self.res_name = res_name
        self.res_describe = res_describe
    def __repr__(self):
        return '(%d,%s,%s)' % (self.res_id,self.res_name, self.res_describe)
if __name__ == "__main__":
    db.create_all()