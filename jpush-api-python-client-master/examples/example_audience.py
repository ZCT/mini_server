import jpush as jpush
from conf import app_key, master_secret
_jpush = jpush.JPush(app_key, master_secret)

push = _jpush.create_push()
push.audience = jpush.audience(
            # jpush.tag("tag1", "tag2"),
            jpush.alias("123456")
        )
push.notification = jpush.notification(android ={
             "alert" : "hello, JPush!", 
             "title" : "JPush test", 
             "builder_id" : 3, 
             "extras" : {
                  "news_id" : 134, 
                  "my_key" : "a value"
             }
        })
push.platform = jpush.all_
push.send()
