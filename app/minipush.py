#coding:utf-8

__author__ = 'cocotang'

import xinge

def BuildNotification(title="onepeice", content="ihome", extra={}, activity=3):
    msg = xinge.Message()
    msg.type = xinge.Message.TYPE_NOTIFICATION
    msg.title = title
    msg.content = content
    msg.expireTime = 3600

    msg.custom = extra

    style = xinge.Style(2, 1, 1, 0, 0)
    msg.style = style

    action = xinge.ClickAction()
    action.actionType = xinge.ClickAction.TYPE_ACTIVITY
    action.activity = activity

    msg.action = action

    return msg


# 按token推送
def DemoPushToken(x,token, msg):
    # 第三个参数environment仅在iOS下有效。ENV_DEV表示推送APNS开发环境
    ret = x.PushSingleDevice(token, msg, xinge.XingeApp.ENV_DEV)
    return ret


# 按app推送
def DemoPushAll(x,msg):
    # 第三个参数environment仅在iOS下有效。ENV_DEV表示推送APNS开发环境
    ret = x.PushAllDevices(xinge.XingeApp.DEVICE_ALL, msg, xinge.XingeApp.ENV_DEV)
    return ret

# 按tag推送
def DemoPushTags(x, msg,tags):
    # 第三个参数environment仅在iOS下有效。ENV_DEV表示推送开发环境
    ret = x.PushTags(xinge.XingeApp.DEVICE_ALL, tags, 'OR', msg, xinge.XingeApp.ENV_DEV)
    return ret



# token-标签绑定
def DemoBatchSetTag(x,tag,token):
    # 切记把这里的示例tag和示例token修改为你的真实tag和真实token
    pairs = []
    pairs.append(xinge.TagTokenPair(tag,token))
    #pairs.append(xinge.TagTokenPair("tag2","f49503f41ebc5b8c44ebac5c75550047a22412a1"))
    ret = x.BatchSetTag(pairs)
    return ret

# token-标签解绑
def DemoBatchDelTag(x,tag,token):
    # 切记把这里的示例tag和示例token修改为你的真实tag和真实token
    pairs = []
    pairs.append(xinge.TagTokenPair(tag,token))
    #pairs.append(xinge.TagTokenPair("tag2","token00000000000000000000000000000000002"))
    ret = x.BatchDelTag(pairs)
    return ret
# 查询token绑定的标签
def DemoQueryTokenTags(x,token):
    # 请把这里示例token修改为你的真实token
    ret = x.QueryTokenTags(token)
    return ret

# 查询标签绑定的设备数
def DemoQueryTagTokenNum(x,tag):
    # 请把这里示例tag修改为你的真实tag
    ret = x.QueryTagTokenNum(tag)
    return ret
