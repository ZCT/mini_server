#coding:utf-8
__author__ = 'cocotang'

import time,datetime

SafeFlag=-2014
def SafeInt( input ):
    if str(input).isdigit():
        input=int(input)
    else:
        input=SafeFlag
    return input


def stamp_date(timestamp):      #将时间戳转换为datetime格式
    tmp = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(timestamp))
    return datetime.datetime.strptime(tmp,'%Y-%m-%d %H:%M:%S')

def date_stamp(date_time):
    return long(time.mktime(date_time.timetuple()))  #将datetime转换为时间戳,


def DebugVerifyId(user_id,g_user_id):
    pass


