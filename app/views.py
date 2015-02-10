#coding:utf-8
__author__ = 'cocotang,yulongwang,alistairyao'

import os, sys
from functools import wraps
from flask import flash,  url_for, request, g, jsonify,json
from app import app ,db, push,xg_push, cache
import datetime
import models, mypush, minipush, myfunc
from mytoken import Token, GetIdFromToken
import random, time
from db_interface import *
from PIL import Image
from werkzeug import secure_filename



reload(sys)
sys.setdefaultencoding('utf-8')




def GenTag(group_id):
    if group_id:
        return "tag"+str(group_id)
    else:
        return "tag"


def GetUserByToken(access_token):
    current_user=cache.get(access_token)
    if current_user is None:
        current_user=models.user_info.query.filter(models.user_info.access_token==access_token).first()
        cache.set(access_token, current_user,timeout=10*60)
    return current_user



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # token=request.args.get('access_token','')
        token=request.form.get('access_token')
        current_user=GetUserByToken(token)               #### 加入新的memcahe模块增加的语句
        #current_user=models.user_info.query.filter_by(access_token=token).first()
        #current_user=models.user_info.query.all()[0]

        if current_user is None:
            return jsonify(
                req_code=-1,
                req_des=u"请先登录"
            )
        elif ((datetime.datetime.now()-current_user.token_update_time).days>300):   #the token is exceeds the life time
             return jsonify(
                 req_code=-2,
                 req_des="token exceed the life time"
             )
        #print current_user.uin
        g.user_id=GetIdFromToken(token)
        return f(*args, **kwargs)
    return decorated_function




def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']




@app.route('/login',methods=['POST'])
def login():
    # open_id = request.args.get('open_id', '')
    # client_token = request.args.get('access_token','')
    open_id=request.form.get('open_id')
    client_token=request.form.get('access_token')
    xgpush_token=request.form.get('xgpush_token')
    if open_id and client_token and xgpush_token:
        current_user=models.user_info.query.filter_by(openid=open_id).first()  #用openId来查

        if not current_user:                    #first login
            current_user=models.user_info(openid=open_id,xgpush_token=xgpush_token)
            db.session.add(current_user)
            db.session.commit()
        else:
            if xgpush_token==current_user.xgpush_token:     #token和原来的相等
                pass
            else:
                current_user.xgpush_token=xgpush_token
                token_user=models.user_info.query.filter_by(xgpush_token=xgpush_token).first()
                if token_user:   #这个token以前有人在用
                    token_user.xgpush_token=None   #清空掉原先用户的token

        server_token=Token(current_user.uin)
        cache.set(server_token.token, current_user,timeout=10*60)                  ######新加入memcache模块增加的语句 ，应该还要增加删除旧的记录的模块
        current_user.access_token=server_token.token
        db.session.add(current_user)
        db.session.commit()
        current_group_ids=[current_group.grp_id for current_group in current_user.groups]
        if current_user.profile_state==0:
            return jsonify(
                req_code=1,
                user_id=current_user.uin,
                access_token=server_token.token,
                profile_state=current_user.profile_state,
                group_ids =current_group_ids,
                avatar_addr=current_user.avatar_addr
                )
        else:
            return jsonify(
                req_code=1,
                user_id=current_user.uin,
                access_token=server_token.token,
                profile_state=current_user.profile_state,
                group_ids =current_group_ids,
                avatar_addr=current_user.avatar_addr,
                user_name=current_user.name,
                user_phone=current_user.phone_number,
                user_birth=current_user.birthday.strftime("%Y-%m-%d")
            )
    else:                               #login failed
        return jsonify(
            req_code=-1,
            req_des=u"登录失败，请重试！"
        )





@app.route('/profile/create',methods=['POST'])
@login_required
def CreateProfile():
    user_name=request.form.get('user_name')
    user_phone=request.form.get('user_phone')
    user_birthday=request.form.get('user_birthday')
    pic_file=request.files['profile_pic']
    if user_name and user_phone and user_birthday:
        current_user=models.user_info.GetUserInfoById(g.user_id)
        current_user.name=user_name
        current_user.phone_number=user_phone
        current_user.birthday=datetime.datetime.strptime(user_birthday,'%Y-%m-%d')
        current_user.profile_state=1
        if pic_file:
            current_user.avatar_addr=app.config['UPLOAD_PROFILE_FOLDER']+str(long(time.time()))+'_'+pic_file.filename
            pic_file.save(app.config['UPLOAD_DIR_ROOT']+current_user.avatar_addr)
        current_group_ids = [ current_group.grp_id for current_group in current_user.groups]
        db.session.add(current_user)
        db.session.commit()
        return jsonify(
            req_code=1,
            profile_state=current_user.profile_state,
            avatar_addr=current_user.avatar_addr,
            user_name=current_user.name,
            user_phone=current_user.phone_number,
            user_birth=current_user.birthday.strftime("%Y-%m-%d")
        )
    else:
        return jsonify(
            req_code=-1,
            req_des="the information is incomplete"
        )




@app.route('/group/create', methods=['POST'])
@login_required
def CreateGroup():
    group_name=request.form.get('grp_name')
    group_desc=request.form.get('grp_desc')
    group_id=random.randint(100000,999999)
    current_user=models.user_info.query.filter_by(uin=g.user_id).first()
    minipush.DemoBatchSetTag(xg_push, GenTag(group_id),current_user.xgpush_token)
    while (models.group_info.query.filter_by(grp_id=group_id).first()):
        group_id=random.randint(100000,999999)
    #group_name=request.args.get('grp_name','')

    current_grp=models.group_info(group_id, create_time=datetime.date.today(), grp_name=group_name, creator_uin=g.user_id,grp_desc=group_desc)
    current_grp.members.append(current_user)
    #current_grp_mem=models.grp_member(group_id, g.user_id)

    db.session.add(current_grp)
    db.session.commit()
    return jsonify(
        req_code = 1,
        group_id = group_id
    )





@app.route('/group/add', methods=['POST'])
@login_required
def AddGroup():
    #group_id=request.args.get('grp_id','')
    group_id=myfunc.SafeInt(request.form.get('grp_id'))
    if group_id==myfunc.SafeFlag:
        return jsonify(
            req_code=-4,
            req_des=u"ID格式不正确"
        )
    #add_user_id=request.args.get('user_id','')
    current_grp=models.group_info.query.filter_by(grp_id=group_id).first()
    if (current_grp):
        current_user=models.user_info.query.filter_by(uin=g.user_id).first()
        create_user=models.user_info.query.filter_by(uin=current_grp.creator_uin).first()       ##查找创建者的信息，这一句可以优化
        for t_group in current_user.groups:
            if t_group.grp_id==group_id:
                return jsonify(
                    req_code=-7,
                    req_des=u"您已经是群成员了，不能再次加入!"
                )
        try:
            extras={"push_code":1,"add_user_id":g.user_id, "add_user_name":current_user.name, "add_user_phone":current_user.phone_number, "group_id":group_id, "group_name":current_grp.grp_name,"avatar_addr":current_user.avatar_addr}
            msg=minipush.BuildNotification(title=u"申请加入family",extra=extras, activity="com.tx.onepiece.activity.VerifyGroupActivity")
            ret=minipush.DemoPushToken(xg_push, create_user.xgpush_token, msg)
           # mypush.PushAlias(current_grp.creator_uin ,title="add group",\
           #                 extras={"push_code":1,"add_user_id":g.user_id,"add_user_name":current_user.name,"add_user_phone":current_user.phone_number,"group_id":group_id,"group_name":current_grp.grp_name})
        except Exception:
            return jsonify(
                req_code=-10,
                req_des="push failed"
            )
        if ret[0]==0:
            return jsonify(req_code=1, req_des=u"等待验证")
        else:
            return jsonify(req_code=ret[0]-100,req_des=ret[1])
        # push.platform = jpush.all_
        # push.send()
    else:
        return jsonify(
            req_code=-1,
            req_des="the group is not existed"
        )




@app.route('/group/verify',methods=['POST'])
@login_required
def VerifyGroupRequest():
    verify_result=myfunc.SafeInt(request.form.get('verify_result'))
    new_user_id=myfunc.SafeInt(request.form.get('new_user_id'))
    group_id=myfunc.SafeInt(request.form.get('group_id'))
    current_group=models.group_info.query.filter_by(grp_id=group_id).first()
    current_user=models.user_info.query.filter_by(uin=new_user_id).first()
    ret=()
    try:
        if verify_result:
            current_group.members.append(current_user)              #这个地方即使推送失败，也要加入数据中  #  多对多关系一定要记得加这句
            minipush.DemoBatchSetTag(xg_push, GenTag(group_id), current_user.xgpush_token)
            #current_group.members.append(models.user_info.GetUserInfoById(new_user_id))
            db.session.add(current_group)
            db.session.commit()
            extras={"push_code":2,"group_name":current_group.grp_name,"group_id":current_group.grp_id,"verify_result":verify_result}
            msg=minipush.BuildNotification(title=u"欢迎加入family",extra=extras,activity="com.tx.onepiece.activity.ResultGroupActivity")
            ret=minipush.DemoPushToken(xg_push, current_user.xgpush_token, msg)

            #mypush.PushAlias(new_user_id,title="admit to new group", extras={"push_code":2,"group_name":current_group.grp_name,"verify_result":verify_result})
            # push.audience = jpush.audience(
            #     jpush.alias(new_user_id)
            # )
            # push.notification = jpush.notification(android ={
            #     "alert" : "hello, Family!",
            #     "title" : "admit to new group",
            #     "builder_id" : 3,
            #     "extras" : {
            #          "group_name":current_group.grp_name
            #         }
            #     })
            # push.platform = jpush.all_
            # push.send()
        else:
            extras={"push_code":3,"group_name":current_group.grp_name,"group_id":current_group.grp_id,"verify_result":verify_result}
            msg=minipush.BuildNotification(title="审核未通过",extra=extras,activity="com.tx.onepiece.activity.ResultGroupActivity")
            ret=minipush.DemoPushToken(xg_push, current_user.xgpush_token, msg)
    except Exception:
        return jsonify(
            req_code=-10,
            req_des='push failed'
        )
    if ret[0]==0:
        return jsonify(req_code=1,req_des=u"成功加入")
    else:
        return jsonify(req_code=ret[0]-100,req_des=ret[1])



@app.route("/groupinfo/query", methods=['POST'])
@login_required
def GetGroupsInfo():
    current_user=models.user_info.query.filter(models.user_info.uin==g.user_id).first()
    ret_data={}
    my_groups=[]
    for c_group in current_user.groups:
        temp={}
        temp['grp_id']=c_group.grp_id
        temp['grp_name']=c_group.grp_name
        temp['grp_desc']=c_group.grp_desc
        temp['creator_uin']=c_group.creator_uin
        my_groups.append(temp)
    ret_data['groups_info']=my_groups
    ret_data['req_code']=1
    return json.dumps(ret_data)





@app.route('/alarms/send',methods=['POST'])
@login_required
def SendAlarms():
    if request.method == 'POST':
        send_user_id=myfunc.SafeInt(request.form.get('send_user_id'))
        send_user=models.user_info.GetUserInfoById(send_user_id)                    #这里需要判断用户是否存在，后面再加判断
        if send_user is None:
            return jsonify(
                req_code=-5,
                req_des=u"接收用户不存在"
                )
        recv_user_id=myfunc.SafeInt(request.form.get('recv_user_id'))
        alarm_time=datetime.datetime.strptime(request.form.get('alarm_time'),'%Y-%m-%d %H:%M:%S') #日期格式转换
        alarm_title=request.form.get('alarm_title')
        current_user=models.user_info.query.filter_by(uin=recv_user_id).first()
        file=request.files['file']
        #print file.filename
        if file and allowed_file(file.filename):
            #filename=str(time.time())+secure_filename(file.filename)
            filepath=os.path.join(app.config['UPLOAD_ALARM_FOLDER'],file.filename)
            try:
                file.save(app.config['UPLOAD_DIR_ROOT']+filepath)     #文件保存一定要加app.config['UPLOAD_DIR_ROOT']
            except IOError:
                return jsonify(
                    req_code=-9,
                    req_des="file save failed"
                    )

            alarm_ct=datetime.datetime.now()
            #recv_user=user_info.GetUserInfoById(recv_userid)
            #create_time=datetime.datetime.today()
            current_alarm=models.alarm_info(from_uin=send_user_id,to_uin=recv_user_id, alarm_title=alarm_title, alarm_datetime=alarm_time, create_time=alarm_ct, alarm_content=filepath)
            # db.session.add(current_alarm)   #调试可以把这两句取消注释，提前加入，以便导入数据到数据库中
            # db.session.commit()                                                         #这里的异常处理机制需不需考虑？
            try:
                extras={"push_code":4,"send_user":send_user.name,"file_path":filepath}
                msg=minipush.BuildNotification(title=u"温馨提醒",extra=extras)
                ret=minipush.DemoPushToken(xg_push, current_user.xgpush_token, msg)

                #mypush.PushAlias(recv_user_id,title="alarm",extras={"push_code":4,"send_user":send_user.name,"file_path":filepath})
            except Exception:
                return jsonify(
                    req_code=-1,
                    req_des='push failed'
                )
            if ret[0]==0:
                db.session.add(current_alarm)
                db.session.commit()                                                         #这里的异常处理机制需不需考虑？
                return jsonify(req_code=1, alarm_id=current_alarm.alarm_id)
            else:
                return jsonify(req_code=ret[0]-100,req_des=ret[1])

        else:
            return jsonify(
                req_code=-1,
                req_des="file upload failed"
            )





@app.route('/alarms/query',methods=['POST'])
@login_required
def QueryAlarms():
    last_alarm_id=myfunc.SafeInt(request.form.get('last_alarm_id'))
    query_action=myfunc.SafeInt(request.form.get('query_action'))      #这里有个bug,上面那个可以传数据过来时可以自动转换成int行的，但这个不行
   # print query_action
    if query_action == 0:         #0 查自己发送的
        query_alarms=models.alarm_info.query.filter(models.alarm_info.from_uin == g.user_id, models.alarm_info.alarm_id >last_alarm_id)
    elif query_action == 1 :                        #1 查自己接收的
        query_alarms=models.alarm_info.query.filter(models.alarm_info.to_uin == g.user_id, models.alarm_info.alarm_id > last_alarm_id)
    else:
        query_alarms=models.alarm_info.query.filter(models.alarm_info.alarm_id > last_alarm_id)
    result={}
    ret_alarm=[]
    for c_alarm in query_alarms:
        ret_alarm.append({"alarm_id":c_alarm.alarm_id,"from_uin":c_alarm.from_uin,"to_uin":c_alarm.to_uin,"alarm_datetime":c_alarm.alarm_datetime.strftime("%Y-%m-%d %H:%M:%S"),\
                       "alarm_title":c_alarm.alarm_title,"create_time":c_alarm.create_time.strftime("%Y-%m-%d %H:%M:%S"),"alarm_content":c_alarm.alarm_content})
    result['ret_code']=1
    result['alarms_list']=ret_alarm
    return json.dumps(result)






#获取联系人列表
@app.route('/family_circle_contacts', methods=['POST'])
@login_required
def GetFamilyList():
    group_id=0
    user_id=myfunc.SafeInt(request.form.get("user_id"))
    group_id=myfunc.SafeInt(request.form.get("group_id"))
    ret_data={}

    current_user=models.user_info.query.filter_by(uin=g.user_id).first()
    if current_user is None:
        ret_data["req_code"]=-1
        ret_data["req_des"]=u"当前用户不存在"
        return json.dumps(ret_data)

    family_list=[]

    for t_group in current_user.groups:
        print t_group.grp_id
        if group_id==0:
            family_list.extend(t_group.members)
        else:
            if group_id==t_group.grp_id:
                family_list.extend(t_group.members)
    family_list=list(set(family_list))

    t_member=[]
    for t_family in family_list:
        temp={}
        temp["user_id"]=t_family.uin
        temp["name"]=t_family.name
        temp["phone_number"]=t_family.phone_number
        temp["avatar_addr"]=t_family.avatar_addr
        temp["birthday"]=t_family.birthday.strftime("%Y-%m-%d")
        t_member.append(temp)
    ret_data["contact_list"]=t_member
    ret_data["req_code"]=1
    ret_data["req_des"]=u"成功获取"
    return json.dumps(ret_data)





#获取联系人照片
@app.route('/family_album_person', methods=['POST'])
@login_required
def GetFamilyAlbum():
    user_id=myfunc.SafeInt(request.form.get('user_id'))
    current_user=models.user_info.query.filter(models.user_info.uin==user_id).first()
    target_user_id=myfunc.SafeInt(request.form.get('target_user_id'))
    max_count=request.form.get('max_count')

    family_albums=models.group_dynamics.query.filter(models.group_dynamics.uin==target_user_id).limit(max_count)

    ret_data={}
    album_list=[]
    for family_album in family_albums:
        temp={}
        temp["photo_url"]=family_album.photo_url
        temp["voice_url"]=family_album.voice_url
        if family_album.timestamp:
            temp["timestamp"]=date_stamp(family_album.timestamp)
        temp["photo_thumbnail"]=family_album.photo_thumbnail
        temp["avatar"]=current_user.avatar_addr
        temp["group_id"]=0
        temp["group_name"]=""
        album_list.append(temp)

    ret_data["album_list"]=album_list
    ret_data["req_code"]=1
    ret_data["req_info"]=u"成功获取"
    return json.dumps(ret_data)


#-------------------------------------------------
# def stamp_date(timestamp):      #将时间戳转换为datetime格式
#     tmp = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(timestamp))
#     return datetime.datetime.strptime(tmp,'%Y-%m-%d %H:%M:%S')
#
# def date_stamp(date_time):
#     return long(time.mktime(date_time.timetuple()))  #将datetime转换为时间戳,





#-------------------------------------------------
#拉取
@app.route('/dynamic/query', methods=['POST'])
@login_required
def GetFamilyDynamic():
    resp = {'req_code':1,'req_info':'success!'}  #初始话状态码
    uin=myfunc.SafeInt(request.form.get('user_id'))
    group_id=myfunc.SafeInt(request.form.get('group_id'))
    c_time=float((request.form.get('last_newest_ts')))
    num=myfunc.SafeInt(request.form.get('max_count'))
    action=request.form.get('action')

    if uin < 0:
        resp['req_code'] = -1
        resp['req_info'] = 'uin_error'
        res = json.dumps(resp)
        return res
    if group_id < 0:
        resp['req_code'] = -1
        resp['req_info'] = 'group_id_error'
        res = json.dumps(resp)
        return res
    if num < 0:
        resp['req_code'] = -1
        resp['req_info'] = 'num_error!'
        res = json.dumps(resp)
        return res
    if c_time < 0:
        resp['req_code'] = -1
        resp['req_info'] = 'timestamp_error!'
        res = json.dumps(resp)
        return res

    act = True  # 默认是刷新
    if "down" == action:
        act = False

    c_time = myfunc.stamp_date(c_time)  # 转换为datetime格式
    groups_id=[]
    if 0 == group_id:       # 当group_id==0时，默认把所在群的更新照片全发送给前端
        groups_id = get_groups_id(uin)
    else:
        groups_id = [group_id]
    results = get_dynamics(groups_id, c_time, num, act)

    lenght = len(results)
    if num < lenght:
        results = results[0:num]
        lenght = num
    for Len in range(0, lenght):
        results[Len]['timestamp'] = myfunc.date_stamp(results[Len]['timestamp'])
    resp['album_list'] = results
    res = json.dumps(resp)
    return res



#获取数据
@app.route('/dynamic/send',methods=['POST'])
@login_required
def SendFamilyDynamic():
    c_time = float(time.time())
    tname = str(long(c_time))
    resp = {'req_code':1,'req_info':'success!'}     #初始话状态码
    uin = myfunc.SafeInt(request.form.get('uin'))
    group_id = myfunc.SafeInt(request.form.get('group_id'))

    current_user=models.user_info.query.filter(models.user_info.uin==uin).first()

    date_c_time = myfunc.stamp_date(c_time)  # 转换为datetime格式

    if uin < 0 or current_user is None:
        resp['req_code'] = -1
        resp['req_info'] = 'uin_error'
        res = json.dumps(resp)
        return res

    if group_id < 0:
        resp['req_code'] = -1
        resp['req_info'] = 'group_id_error'
        res = json.dumps(resp)
        return res
    #uploaded_files=request.files.getlist("file[]")
    photo_file = request.files['photo_file']
    if photo_file and allowed_file(photo_file.filename):
        photo_name = secure_filename(photo_file.filename)
        photo_name = str(uin)+tname + photo_name
        photo_url = os.path.join(app.config['UPLOAD_PICTURE_FOLDER'],photo_name)
        photo_file.save(app.config['UPLOAD_DIR_ROOT']+photo_url)   #存储大图

        photo_file = Image.open(app.config['UPLOAD_DIR_ROOT']+photo_url)
        w,h = photo_file.size
        if w > h:
            lenght = h
            region = ((w-h)/2,0,(w+h)/2,h)
        else:
            lenght = w
            region = (0,(h-w)/2,w,(h+h)/2)           #获取切割正方形区域
        photo_crop = photo_file.crop(region)

        if lenght < 200:
            photo_mini = photo_crop
        else:
            photo_mini = photo_crop.resize((200,200),Image.BILINEAR)
        photo_thumbnail = os.path.join(app.config['UPLOAD_MINIPIC_FOLDER'],photo_name)
        photo_mini.save(app.config['UPLOAD_DIR_ROOT']+photo_thumbnail)                                       #存储小图
    else:                        # 上传不是图片
        resp['req_code'] = -1
        resp['req_info'] = 'no_picture !'
        res = json.dumps(resp)
        return res

    voice_file = request.files.get('voice_file',"")
    voice_url=""
    if voice_file and allowed_file(voice_file.filename):        # return res  #if

        voice_name = secure_filename(voice_file.filename)
        voice_name = str(uin)+tname + voice_name
        voice_url = os.path.join(app.config['UPLOAD_VOICE_FOLDER'],voice_name)
        voice_file.save(app.config['UPLOAD_DIR_ROOT']+voice_url)
    # elif voice_file is None:              #只上传图片，未上传语音，voice_url地址储存为None
    #     voice_url = None
    else:
        resp['req_code'] = 1
        resp['req_info'] = 'not_voice !'
        res = json.dumps(resp)

    resp['photo_url'] = photo_url
    resp['photo_thumbnail'] = photo_thumbnail
    resp['voice_url'] = voice_url
    resp['timestamp']=c_time
    resp['nick_name']=current_user.name
    resp['avatar']=current_user.avatar_addr
    resp['group_name']=""

    if 0 == group_id:                  #当group_id == 0时，默认把图片发表到所在的所有群中
        resp['group_id']=0
        #print group_id
        groups_id = get_groups_id(uin)
        print uin
        post_dynamic(uin,groups_id,photo_url,voice_url,photo_thumbnail,date_c_time)   #这个函数接口还有问题，需要统一
    else:
        resp['group_id']=group_id                    #把图片发表到指定的群中
        grp_id=[group_id]
        post_dynamic(uin,grp_id,photo_url,voice_url,photo_thumbnail, date_c_time)
    res = json.dumps(resp)
    return res














