#coding:utf-8
__author__ = 'cocotang'


import requests
import time
import datetime



#files = {'image01': open('01.jpg', 'rb')}
user_info = {'name': 'letian'}

#r=requests.post("http://203.195.164.20:5000/group/create?grp_name=onepiece&access_token=PdBacY6WTEKXHSWB0E3Z2zJ8d")

#r = requests.get("http://127.0.0.1:5000/upload", data=user_info, files=files)

# 创建用户
pay_load={'open_id':'837EBE497DA386DBCC8F0869sfef', 'access_token':'sgegeasgeghgh','xgpush_token':'ce87900e132e1e09487ea45545d9a56512accf22'}
r=requests.post("http://203.195.164.20:5000/login", data=pay_load)

# 1=K6i1HZ821WGK00JGMEBe6JAKz
# 2=Ev2Fn0XyaA6NJlRwu0aD7NZcs
# 3=geeeeeeeeeeeeeeeeeeeee


# 8=Lenx0SZYPPygIHeC9M09omS0r
# 11=tjBjEO1LfRYblTpN3OTSEnT3zz
#创建群

# cocofamily=565891
# pay_load={'access_token':'Lenx0SZYPPygIHeC9M09omS0r','grp_name':'cocofamily'}
# r=requests.post("http://203.195.164.20:5000/group/create", data=pay_load)

#1 381732
#加入群
# pay_load={'access_token':'tjBjEO1LfRYblTpN3OTSEnT3zz','grp_id':'565891'}
# r=requests.post("http://203.195.164.20:5000/group/add", data=pay_load)

#查群组信息
# pay_load={'access_token':'3kh2sZrTuPCOb9CWq8zw60lxzg'}
# r=requests.post("http://203.195.164.20:5000/groupinfo/query", data=pay_load)

#审核
# pay_load={'access_token':'Ev2Fn0XyaA6NJlRwu0aD7NZcs','verify_result':0, 'new_user_id':2, 'group_id':381732}
# r=requests.post("http://203.195.164.20:5000/group/verify", data=pay_load)


# 填写资料
# pay_load={'user_name':'coco', 'access_token':'Ev2Fn0XyaA6NJlRwu0aD7NZcs','user_phone':'33rrg','user_birthday':'2014-02-03'}
# upload_file = {'profile_pic': ('upload_test2.txt', open('upload_test.txt', 'rb'))}
# r=requests.post("http://203.195.164.20:5000/profile/create", data=pay_load, files=upload_file)
# #
#
#
# # # 消息提醒
# pay_load={'send_user_id':'1', 'access_token':'K6i1HZ821WGK00JGMEBe6JAKz','recv_user_id':2,'alarm_time':'2014-02-03 09:30:33'}
# upload_file = {'file': ('upload_test3.txt', open('upload_test.txt', 'rb'))}
# r=requests.post("http://203.195.164.20:5000/alarms/send", data=pay_load, files=upload_file)


# 消息查询
# pay_load={'last_alarm_id':2, 'query_action':1,'access_token':'3kh2sZrTuPCOb9CWq8zw60lxzg'}
# r=requests.post("http://203.195.164.20/alarms/query", data=pay_load)


# # 联系列表
# pay_load={'user_id':21, 'group_id':0,'access_token':'Phnw51kh0rC3QuoRzVhzUBkNsz'}
# r=requests.post("http://203.195.164.20/family_circle_contacts", data=pay_load)
#

#家人圈动态查询
# BgaSqTX0PecNqgVi5o2WQlxezr
# 18
# c_time=long(time.time())
# pay_load={'user_id':15, 'access_token':'3kh2sZrTuPCOb9CWq8zw60lxzg','max_count':4,'action':'down','group_id':0,'last_newest_ts':1504288932.756}
# r=requests.post("http://203.195.164.20/dynamic/query", data=pay_load)

#家人圈动态发送
# pay_load={'uin':15, 'access_token':'3kh2sZrTuPCOb9CWq8zw60lxzg','group_id':0}
# upload_file ={'photo_file': ('test.jpg', open('test.jpg', 'rb'))}
# r=requests.post("http://203.195.164.20:5000/dynamic/send", data=pay_load, files=upload_file)

#获取个人相册
# pay_load={'user_id':1,'target_user_id':1, 'access_token':'K6i1HZ821WGK00JGMEBe6JAKz','max_count':5}
# r=requests.post("http://203.195.164.20/family_album_person", data=pay_load)

#pay_load={'grp_id':'224642', 'access_token':'lFa0LETbdIOm0ageb7VHEjWFz'}
# r=requests.post("http://203.195.164.20:5000/group/add", data=pay_load)

# upload_file = {'file': ('upload_test.txt', open('upload_test.txt', 'rb'))}
# pay_load={'recv_user_id':'2', 'access_token':'K6i1HZ821WGK00JGMEBe6JAKz','alarm_time':'2014-06-23 17:34:00'}
# r=requests.post("http://203.195.164.20:5000/alarms/send", data=pay_load, files=upload_file)

#测试nginx
# r = requests.get("http://203.195.164.20/login")


#测试时间
# import datetime
#
# def stamp_date(timestamp):      #将时间戳转换为datetime格式
#     tmp = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(timestamp))
#     return datetime.datetime.strptime(tmp,'%Y-%m-%d %H:%M:%S')
#
# def date_stamp(date_time):
#     return long(time.mktime(date_time.timetuple()))  #将datetime转换为时间戳,
#
# c=1404288932.756
#
# print stamp_date(c)

print r.text
