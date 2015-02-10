#coding:utf-8
__author__ = 'cocotang,yulongwang,alistairyao'


from hashlib import md5
from app import db
from app import app
import datetime


grp_member = db.Table('grp_member',\
        db.Column('grp_id',db.Integer,db.ForeignKey('group_info.grp_id')),\
        db.Column('uin',db.Integer,db.ForeignKey('user_info.uin'))\
)

class user_info(db.Model):
    uin = db.Column(db.Integer, primary_key=True)
    openid = db.Column(db.String(128))
    access_token = db.Column(db.String(128))
    name = db.Column(db.String(128))
    phone_number = db.Column(db.String(30))
    birthday = db.Column(db.DateTime)
    avatar_addr = db.Column(db.Text(128))
    profile_state=db.Column(db.Integer)
    xgpush_token=db.Column(db.String(128))
    token_update_time=db.Column(db.DateTime)

    def __init__(self, name=None, phone_number=None, birthday=None, avatar_addr=None, openid=None, access_token=None, xgpush_token=None,profile_state=0,token_update_time=datetime.datetime.now()):
        self.access_token=access_token
        self.name=name
        self.phone_number=phone_number
        self.birthday=birthday
        self.avatar_addr=avatar_addr
        self.openid=openid
        self.xgpush_token = xgpush_token
        self.profile_state = profile_state
        self.token_update_time=token_update_time

    @staticmethod
    def GetUserInfoById(user_id):
        return user_info.query.filter_by(uin=user_id).first()

    @staticmethod
    def GetUserInfoByToken(token):
        return user_info.query.filter_by(access_token=token).first()

    def family(self):
        family = list()
        for group in self.groups:
            family.extend(group.members)
        family = list(set(family))
        return family



class group_info(db.Model):
    grp_id=db.Column(db.Integer, primary_key = True)
    grp_name=db.Column(db.String(128))
    create_time=db.Column(db.Date)
    creator_uin=db.Column(db.Integer,db.ForeignKey("user_info.uin"))
    grp_desc=db.Column(db.String(128))
    members = db.relationship('user_info',\
        secondary = grp_member,\
	backref = db.backref('groups', lazy = 'dynamic'),\
	lazy = 'dynamic')


    def __init__(self,grp_id, grp_name=None, create_time=None, creator_uin=None,grp_desc="one piece"):
        self.grp_id=grp_id
        self.grp_name=grp_name
        self.create_time=create_time
        self.creator_uin=creator_uin
        self.grp_desc=grp_desc

    def accept(self,user):
        if not self.is_member(user):
            self.members.append(user)
        return self

    def is_member(self,user):
        return self.members.filter(grp_member.c.uin==user.uin).count() > 0


class alarm_info(db.Model):
    alarm_id=db.Column(db.Integer, primary_key=True)
    from_uin=db.Column(db.Integer,db.ForeignKey("user_info.uin"))
    to_uin=db.Column(db.Integer, db.ForeignKey("user_info.uin"))
    alarm_datetime=db.Column(db.DateTime)
    alarm_title=db.Column(db.String(30))
    create_time=db.Column(db.DateTime)
    alarm_content=db.Column(db.String(128))

    def __init__(self, from_uin=None, to_uin=None, alarm_datetime=None, alarm_title=None, create_time=None, alarm_content=None):
        self.from_uin=from_uin
        self.to_uin=to_uin
        self.alarm_datetime=alarm_datetime
        self.alarm_title=alarm_title
        self.create_time=create_time
        self.alarm_content=alarm_content




class group_dynamics(db.Model):
    dynamic_id = db.Column(db.Integer,primary_key=True)
    group_id = db.Column(db.Integer,db.ForeignKey("group_info.grp_id"))
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
        self.timestamp=timestamp


db.create_all()  #this function is need call when there no table