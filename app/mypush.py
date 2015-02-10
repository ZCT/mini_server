#coding:utf-8
__author__ = 'cocotang'

from app import push
import jpush as jpush

def PushAlias(user_id, alert="hello family", title="one piece", builder_id=3, extras={}):
    push.audience=jpush.audience(
        jpush.alias(user_id)
    )
    push.notification=jpush.notification(
        {               #这里去掉了android=，如果推送有问题，疑点1
            "alert" : alert,
            "title" : title,
            "builder_id" : builder_id,
            "extras" : extras
        }

    )
    push.platform=jpush.all_
    push.send()        #send 返回值问题



def PushTags(tag_ids,alert="hello family", title="one piece", builder_id=3, extras={}):
    push.audience=jpush.audience(
        jpush.tag([tag_id for tag_id in tag_ids])
    )

    push.notification=jpush.notification(
        {                   #这里去掉了android=，如果推送有问题，疑点1
            "alert" : alert,
            "title" : title,
            "builder_id" : builder_id,
            "extras" : extras
        }

    )
    push.platform=jpush.all_
    push.send()             #send 返回值问题