import string
import urllib.request
import re
import os
import urllib
# 根据给定的网址来获取网页详细信息，得到的html就是网页的源代码
import requests
import time

import soup
from PIL import Image
from io import BytesIO

from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter

basePath = "https://www.smashbros.com"
def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    return html.decode('UTF-8')


def getImg(html,path):
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=10))
    s.mount('https://', HTTPAdapter(max_retries=10))

    reg = 'url(.*);'
    imgre = re.compile(reg)
    imglist = imgre.findall(html)

    soup = BeautifulSoup(html, 'html.parser')
    all_img = (soup.find_all('img'))
    for img in all_img:
        src = img['src']
        imglist.append(src)

    # patterncss = '<link rel="stylesheet" href="(.*?)"'
    patterncss = '<link.*?href="(.*?)"'
    hrefList = re.compile(patterncss, re.S).findall(html)
    for href in hrefList:
        if(href.find('http')<0):
            href = basePath+href
        tmpHtml = getHtml(href)
        reg = 'url(.*\.png|jpg);'
        imgre = re.compile(reg)
        imglistTmp = imgre.findall(tmpHtml)
        imglist.extend(imglistTmp)
    x = 0
    if not os.path.isdir(path):
        os.makedirs(path)
    # paths = path+'\\'

    for imgurl in imglist:
        if(imgurl.find('.svg')>0):
            continue;
        if (x >= -1):
            imgurl = imgurl.replace('(', '')
            imgurl = imgurl.replace(')', '')
            nameList = imgurl.split('/');
            name = ''
            for nameTmp in nameList:
                name = nameTmp
            url = basePath + imgurl;
            print(url);
            print('ks')
            #  urllib.request.urlretrieve(url,'{}{}.jpg'.format(paths,x))
            content = ''
            try:
                response = requests.get(url, timeout=3)
                content = response.content
            except Exception as e:
                print(e)
                time.sleep(3)
                response = requests.get(url, timeout=3)
                content = response.content
            try:
                image = Image.open(BytesIO(content))
                savePath = path + name
                print(savePath)
                image.save(savePath)
                print('js')
            except Exception as e:
                print(s)
            x = x + 1
        else:
            x = x + 1
    return imglist

path = 'D:\\test\\itemindex\\'
html = getHtml("https://www.smashbros.com/TC/item/index.html")
getImg(html,path)
path = 'D:\\test\\fighterindex\\'
html = getHtml("https://www.smashbros.com/TC/fighter/index.html")
getImg(html,path)
path = 'D:\\test\\aboutindex\\'
html = getHtml("https://www.smashbros.com/TC/about/index.html")
getImg(html,path)
