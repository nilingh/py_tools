#!/usr/bin/env python3
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
# 自定义图片存放路径
IMG_DIR = "/Users/neil/Pictures/bing_img/"

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