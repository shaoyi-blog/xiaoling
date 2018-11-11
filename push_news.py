#!/usr/bin/python
# -*- coding: utf-8 -*- 

import time
import datetime
import json
import requests
import sys
sys.path.append("./tools/")
import helper
from bs4 import BeautifulSoup



def get_jike_news():
    '''
#抓取即刻上的“一觉醒来世界发生了什么”
    '''
    url = "http://m.okjike.com/topics/553870e8e4b0cafb0a1bef68"
    r = requests.get(url)
    jike_content = r.text
    soup = BeautifulSoup(jike_content, "html.parser")
    new_items = soup.find(class_="message-content" ).find_all("div")
    news = [i.string.encode('utf-8') for i in new_items[1:] if i.string is not None ]
    yesterday_news =  '\n'.join(news).split('(')[0]
    return yesterday_news

if __name__ == '__main__':
    max_wait_time = 3600*2 # 两小时
    retry_time = 300   # 五分钟
    try_time = 0
    while try_time <= max_wait_time:
        news = get_jike_news()
        if  news is None:
            threading.sleep(retry_time)
            try_time += retry_time
        else:
            helper.send_to_wechat( "临溪", '早上好，小令为你播报早间新闻：\n' + news)
            print("今日即可新闻发完了呦～", datetime.datetime.now())
            sys.exit(0)





