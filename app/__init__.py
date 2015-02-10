#coding:utf-8
__author__ = 'cocotang'

import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import PUSH_APP_KEY, PUSH_MASTER_SECRET
import jpush as jpush
import xinge
from werkzeug.contrib.cache import  MemcachedCache

app = Flask(__name__)
app.config.from_object('config')

db=SQLAlchemy(app)
cache = MemcachedCache(['127.0.0.1:11211'])

_jpush = jpush.JPush(PUSH_APP_KEY, PUSH_MASTER_SECRET)
push = _jpush.create_push()

xg_push = xinge.XingeApp(2100036003, '76c861f8e550af0aee2bedd93b840e9a')

from app import views, models



