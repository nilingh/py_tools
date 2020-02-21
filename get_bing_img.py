#!/usr/local/bin/python3
# -*- encoding: utf-8 -*-
'''
Created Date:2020/02/10 15:00:20
Writer: Zhen
'''
from bs4 import BeautifulSoup
import requests
import re
# 要加上/?mkt=zh-CN才能获取到包含图片url的html
URL = "https://www.bing.com/?mkt=zh-CN"
# 定义图片存放路径
IMG_DIR = "/Users/neil/Pictures/bing_img/"
# 定义图片归档目录
IMG_ARC = "/Users/neil/Pictures/bing_img/archive_img/"

# 获取html(测试下来不需要header)
html = requests.get(URL)
soup = BeautifulSoup(html.text, "lxml")
# img_url = soup.find("td", {"id": "hp_cellCenter", "class":"hp_hd"}).find("div", {"id":"hp_container"}).find("div",{"id":"bgDiv"}).find("div")["data-ultra-definition-src"]
# 测试下来可以省略上面部分标签,直接定位
img_url = soup.find("div", {"id": "bgDiv"}).find("div")[
    "data-ultra-definition-src"]
# 获取到图片地址
img_url = "https://www.bing.com/"+img_url
print("img_url: ", img_url)

# 用正则从图片url中提取图片的名称
re_rule = r'OHR\..+?.jpg'
image_name = re.findall(re_rule, img_url)
image_name = image_name[0].split('OHR.')[-1]
print("image_name: ", image_name)

# 下载图片到指定目录
r = requests.get(img_url, stream=True)
with open(IMG_DIR+image_name, 'wb') as f:
    i = 0
    for chunk in r.iter_content(chunk_size=128):
        f.write(chunk)
        i += 1
    print('Saved {} chuncks to {} '.format(i, image_name))

# 将两天前的照片归档, 这样可以每天看新的
import os, datetime, time
import shutil
# 两天前日期,格式datetime
last_2_day = datetime.datetime.now() + datetime.timedelta(days=-2)
# 将datetime转换成time
last_2_time = time.mktime(last_2_day.timetuple())

os.chdir(IMG_DIR)

for img in os.listdir(IMG_DIR):
    # print(img, os.path.getctime(img), last_2_time)
    if os.path.isfile(img) and os.path.splitext(img)[1] == ".jpg" and os.path.getmtime(img) < last_2_time:
        shutil.move(img, IMG_ARC)