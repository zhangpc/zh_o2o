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

class Content_url(db.Model):
    __tablename__ = 'content_url'
    url_id = db.Column(db.Integer, primary_key = True)
    url_blue = db.Column(db.String(150))
    url_red = db.Column(db.String(150))
    url_type = db.Column(db.SmallInteger)
    url_stuts = db.Column(db.SmallInteger)
    sql_id = db.Column(db.Integer,db.ForeignKey('content_sql.sql_id'))
    def __init__(self, url_blue = None,url_red=None,url_type=None,url_stuts = None,sql_id = None):
        self.url_blue = url_blue
        self.url_red = url_red
        self.url_type = url_type
        self.url_stuts = url_stuts
        self.sql_id = sql_id

    def __repr__(self):
        return '(%d,%s,%s,%d,%d,%d)' % (self.url_id,self.url_blue, self.url_red,self.url_type,self.url_stuts,self.sql_id)

    def to_json(self):
        return {
            'url_id': self.url_id,
            'url_blue': self.url_blue,
            'url_red':self.url_red,
            'url_type':self.url_type,
            'url_stuts':self.url_stuts,
            'sql_id':self.url_stuts,
        }

if __name__ == "__main__":
    db.create_all()