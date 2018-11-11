#!/usr/bin/pthon
# -*- coding:utf-8-*-

import itchat
from itchat.content import *
from flask import Flask,request
import threading

'''
itchat + Flask实现 python 发送消息 API
'''

def send_msg_to_user(user_name, msg, msg_type='text'):
    '''
    功能：发送消息给个人
    参数：msg: 消息内容, 图片\文件、视频、类型消息则是文件地址
         msg_type: text、img、file， video
    '''
    try:
        name = itchat.search_friends(name = user_name)
        to_user = name[0]["UserName"]

        msg_pre = ''
        if msg_type == 'file':
            msg_pre = '@fil@'
        elif msg_type == 'img':
            msg_pre = '@img@'
        elif msg_type == 'video':
            msg_pre = '@vid@'
        real_msg = msg_pre + msg
        itchat.send(real_msg, toUserName = to_user)
    except Exception as e:
        return (False, str(e))
    return (True, None)

def send_msg_to_group(group_name, msg, msg_type):
    '''
    功能：发送消息给群组
    参数：msg: 消息内容, 图片\文件、视频、类型消息则是文件地址
         msg_type: text、img、file， video
    '''
    try:
        itchat.get_chatrooms(update=True)
        chatrooms = itchat.search_chatrooms(name=u"机器人测试群")
        print len(chatrooms)
        toUserName = chatrooms[0]['UserName']

        msg_pre = ''
        if msg_type == 'file':
            msg_pre = '@fil@'
        elif msg_type == 'img':
            msg_pre = '@img@'
        elif msg_type == 'video':
            msg_pre = '@vid@'
        real_msg = msg_pre + msg
        itchat.send(real_msg, toUserName = to_user)
    except Exception as e:
        return (False, str(e))
    return (True, None)

def lc():
    send_msg_to_user(u'临溪', u'主人，小令插上电源啦！')



app = Flask(__name__)

MY_URL = '/xiaoling/'

# 发消息给个人账户
@app.route(MY_URL + 'toUser/get/',methods=['GET'])
def sendMsg2User():
    print(request.args.to_dict())  #request.args请求参数
    pram_dict = request.args.to_dict()
    to_user = pram_dict['user_name']
    msg = pram_dict['msg']
    msg_type = pram_dict['msg_type']
    print "%s  %s  %s"%(to_user, msg, msg_type)
    ret = send_msg_to_user(to_user, msg, msg_type)
    print ret
    return "failed because:" + ret[1] if not ret[0] else 'success'

# 发消息给群
@app.route(MY_URL + 'toGroup/get/',methods=['GET'])
def sendMsg2group():
    print(request.args.to_dict())  #request.args请求参数
    pram_dict = request.args.to_dict()
    to_group = pram_dict['group_name']
    msg = pram_dict['msg']
    msg_type = pram_dict['msg_type']
    ret = send_msg_to_group(to_group, msg, msg_type)
    print ret
    return "failed because:" + ret[1] if not ret[0] else 'success'


itchat.auto_login( enableCmdQR=2, loginCallback=lc)
app.run('0.0.0.0', 5000)
#xl_api = threading.Thread(target=app.run, args=('0.0.0.0', 5000), name='xiaoling_api')
#xl_api.setDaemon(True)
#xl_api.start()
#itchat.run(True)