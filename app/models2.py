#coding:utf-8
#Author:alistairyao
#2014.6.28
#This is a database model

from datetime import *
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:onepiece9@10.66.106.13:3306/jiarendb'
db = SQLAlchemy(app)

grp_member = db.Table('grp_member',\
        db.Column('group_id',db.Integer,db.ForeignKey('group_info.group_id')),\
        db.Column('uin',db.Integer,db.ForeignKey('user_info.uin'))\
)

class user_info(db.Model):
    uin = db.Column(db.Integer, primary_key=True)
    openid = db.Column(db.String(128))
    access_token = db.Column(db.String(128))
    nick_name = db.Column(db.String(128))
    phone_number = db.Column(db.String(30))
    birthday = db.Column(db.DateTime)
    avatar = db.Column(db.Text(128))
    album = db.Column(db.Text(128))

    def __init__(self, nick_name=None, phone_number=None, birthday=None, avatar=None, openid=None, access_token=None, album=None):
        self.access_token = access_token
        self.nick_name = nick_name
        self.phone_number = phone_number
        self.birthday = birthday
        self.avatar = avatar
        self.openid = openid
	    self.album = album

    def family(self):
	'''
	Find all the family members, including himself. 
	'''
	family = list()
	for group in self.groups:
		family.extend(group.members)
	family = list(set(family))
	return family 
	
class group_info(db.Model):
    group_id=db.Column(db.Integer, primary_key = True)
    group_name=db.Column(db.String(128))
    create_time=db.Column(db.Date)
    creator_uin=db.Column(db.Integer,db.ForeignKey("user_info.uin"))
    members = db.relationship('user_info',\
        secondary = grp_member,\
	backref = db.backref('groups', lazy = 'dynamic'),\
	lazy = 'dynamic')


    def __init__(self,group_id, group_name=None, create_time=None, creator_uin=None):
        self.group_id=group_id
        self.group_name=group_name
        self.create_time=create_time
        self.creator_uin=creator_uin
    
    def accept(self,user):
	if not self.is_member(user):
		self.members.append(user)
		return self

    def is_member(self,user):
	return self.members.filter(grp_member.c.uin==user.uin).count() > 0

class alarm_info(db.Model):
	alarm_id = db.Column(db.Integer,primary_key=True)
	from_uin = db.Column(db.Integer,db.ForeignKey("user_info.uin"))
	to_uin = db.Column(db.Integer,db.ForeignKey("user_info.uin"))
	alarm_datetime = db.Column(db.DateTime)
        alarm_title = db.Column(db.String(30))
	alarm_content = db.Column(db.String(128))
	
        def __init__(self,from_uin=None, to_uin=None, alarm_datetime=None, alarm_title=None, alarm_content=None):
		self.from_uin = from_uin
		self.to_uin = to_uin
		self.alarm_datetime = alarm_datetime
		self.alarm_title = alarm_title
		self.alarm_content = alarm_content

class sys_alarm_info(db.Model):
        sys_alarm_id = db.Column(db.Integer,primary_key=True)
        to_group_id = db.Column(db.Integer,db.ForeignKey("group_info.group_id"))
        alarm_datetime = db.Column(db.DateTime)
        alarm_content = db.Column(db.String(128))
	
        def __init__(self,to_group_id=None, alarm_datetime=None, alarm_content=None):
                self.to_group_id = to_group_id
                self.alarm_datetime = alarm_datetime
                self.alarm_content = alarm_content

class group_dynamics(db.Model):
	dynamic_id = db.Column(db.Integer,primary_key=True)
	group_id = db.Column(db.Integer,db.ForeignKey("group_info.group_id"))
	uin = db.Column(db.Integer,db.ForeignKey("user_info.uin"))
	photo_url = db.Column(db.String(128))
	voice_url = db.Column(db.String(128))
	photo_thumbnail = db.Column(db.String(128))
	timestamp = db.Column(db.TIMESTAMP)
	
	def __init__(self, group_id=None, uin=None, photo_url=None, voice_url=None, photo_thumbnail=None, timestamp=None):
		self.group_id = group_id
		self.uin = uin
		self.photo_url = photo_url
		self.voice_url = voice_url
		self.photo_thumbnail = photo_thumbnail



