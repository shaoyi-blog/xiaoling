#!/usr/bin/pyhton
#-*- coding:utf-8-*-

import requests
import datetime


def send_to_wechat(username, msg, msg_type='text', is_group = False):
	send_func = 'toUser'
	if is_group:
		send_func ='toGroup'
	api_url = 	"http://207.148.70.133:5000/xiaoling/%s/get/?user_name=%s&msg=%s&msg_type=%s" %( send_func, username,msg,msg_type)
	print api_url
	ret = requests.get(api_url)
	print ret
	if 'success' not in ret:
		print "本次任务执行失败"


# 根据当前日期获取需要的时间： delta 为当前日期加上活着减掉的日期
def get_date(delta):
    today = datetime.datetime.today()
    want_day = today - datetime.timedelta(days=delta)
    return want_day.strftime("%Y-%m-%d")