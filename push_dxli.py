#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
import json
import re
import datetime
import sys
import threading

sys.path.append("./tools/")
import helper

def save_image(image_url):
	file_name = str(datetime.datetime.now())
	pic_path = '/tmp/%s.jpg' %(file_name)
	ir = requests.get(image_url)
	if ir.status_code == 200:
		open(pic_path, 'wb').write(ir.content)
		return pic_path
	return None


def get_danxiangli():
	'''
#抓取 单向历
		'''
	target_url = 'https://app.jike.ruguoapp.com/1.0/messages/history'
	payload = {"loadMoreKey": None, "topic": "58ada0cd9d7b7d001598c4b8", "limit": 20}
	jike_content = requests.post(target_url, json=payload).text
	json_text = json.loads(jike_content)
	content =  json_text[u'data'][0][u'content'].encode('utf-8')
	month = content.split('月')[0].split('#')[2].strip()
	day = content.split('月')[1].split('日')[0].strip()
	if str(datetime.datetime.now().day) == day and str(datetime.datetime.now().month) == month:
		pic_url =  json_text[u'data'][0][u'pictureUrls'][0][u'picUrl']
		return pic_url
	else:
		return None


if __name__ == '__main__':
	max_wait_time = 3600*2 # 两小时
	retry_time = 300   # 五分钟
	try_time = 0
	while try_time <= max_wait_time:
		pic_url = get_danxiangli()
		if  pic_url is None:
			threading.sleep(retry_time)
			try_time += retry_time
		else:
			pic_path = save_image(pic_url)
			if pic_path is None:
				print "任务出错"
				sys.exit(-1)
			helper.send_to_wechat( "临溪", pic_path, msg_type='img')
			print("今日的单向历发完了呦～", datetime.datetime.now())
			sys.exit(-1)


