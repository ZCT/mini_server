#coding:utf-8
__author__ = 'cocotang'

import os
import base64
import string
import random
import myfunc

int2char_dict={'0':'b', '1':'z','2':'s','3':'d','4':'x','5':'g','6':'h','7':'a','8':'r','9':'u'}
char2int_dict={'b':'0', 'z':'1','s':'2','d':'3','x':'4','g':'5','h':'6','a':'7','r':'8','u':'9'}

class Token():
    def __init__(self, user_id):
        chars=string.ascii_letters+string.digits
        self.token=''.join([random.choice(chars) for i in range(24)])
        for sig_char in str(user_id):
            self.token+=int2char_dict[sig_char]
        #self.token=base64.encodestring(self.token)



def GetIdFromToken(token):
    #decode_token=token
    #decode_token=base64.decodestring(token)
    int_str=''
    for sig_char in  token[24:]:
        int_str+=char2int_dict[sig_char]
    return myfunc.SafeInt(int_str)
    #print decode_token
    #return int(decode_token[24:])

if __name__=='__main__':
    s=Token(13)
    print s.token
    print GetIdFromToken(s.token)


