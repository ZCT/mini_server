#coding:utf-8
__author__ = 'cocotang'




from werkzeug.contrib.cache import  MemcachedCache

print "test"
cache = MemcachedCache(['127.0.0.1:11211'])