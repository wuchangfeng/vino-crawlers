#-*- coding: utf-8 -*-
__author__ = 'Wu_cf'

import json
import itertools
import urllib
import requests
import os
import re
import sys
sys.path.append('PIL')
from PIL import Image as im


str_table = {
    '_z2C$q': ':',
    '_z&e3B': '.',
    'AzdH3F': '/'
}

char_table = {
    'w': 'a',
    'k': 'b',
    'v': 'c',
    '1': 'd',
    'j': 'e',
    'u': 'f',
    '2': 'g',
    'i': 'h',
    't': 'i',
    '3': 'j',
    'h': 'k',
    's': 'l',
    '4': 'm',
    'g': 'n',
    '5': 'o',
    'r': 'p',
    'q': 'q',
    '6': 'r',
    'f': 's',
    'p': 't',
    '7': 'u',
    'e': 'v',
    'o': 'w',
    '8': '1',
    'd': '2',
    'n': '3',
    '9': '4',
    'c': '5',
    'm': '6',
    '0': '7',
    'b': '8',
    'l': '9',
    'a': '0'
}

# str 的translate方法需要用单个字符的十进制unicode编码作为key
# value 中的数字会被当成十进制unicode编码转换成字符
# 也可以直接用字符串作为value
char_table = {ord(key): ord(value) for key, value in char_table.items()}

# 解码图片URL
def decode(url):
    # 先替换字符串
    for key, value in str_table.items():
        url = url.replace(key, value)
    # 再替换剩下的字符
    return url.translate(char_table)

# 生成网址列表
def buildUrls(word):
    #底下这种用法是python3.x
   # word = urllib.parse.quote(word)
    #底下这种用法是python2.x
    word = urllib.quote(word)
    url = r"http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&fp=result&queryWord={word}&cl=2&lm=-1&ie=utf-8&oe=utf-8&st=-1&ic=0&word={word}&face=0&istype=2nc=1&pn={pn}&rn=60"
    urls = (url.format(word=word, pn=x) for x in itertools.count(start=0, step=60))
    return urls

# 解析JSON获取图片URL
re_url = re.compile(r'"objURL":"(.*?)"')
def resolveImgUrl(html):
    imgUrls = [decode(x) for x in re_url.findall(html)]
    return imgUrls

def downImg(imgUrl, dirpath, imgName):
    filename = os.path.join(dirpath, imgName)
    try:
        res = requests.get(imgUrl, timeout=15)
        if str(res.status_code)[0] == "4":
            print str(res.status_code), ":" , imgUrl
            return False
    except Exception as e:
        print "抛出异常：", imgUrl
        print e
        return False
    #图片写入文件
    with open(filename, "wb") as f:
        f.write(res.content)
    return True


def mkDir(dirName):
    dirpath = os.path.join(sys.path[0], dirName)
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    return dirpath

def selectImg():
    # 这里路径换成你自己的
    path = 'C:\\Users\\Administrator\\PycharmProjects\\self_spiderLearning\\results\\'
    for x in os.listdir(path):
        if x.endswith('.jpg'):
            # file是图像对象，并没有close（）方法
             try:
                fp = open(path+x,'rb')
                file = im.open(fp)
             except Exception as e:
                 continue
        x1= file.size[0]
        y1= file.size[1]
        print x1,y1 ,x
        fp.close()
        if x1 < y1:
            try:
                os.remove(path+x)
                print "已删除 %s " % x
            except Exception as e:
                print "抛出异常："
                print e




if __name__ == '__main__':
    print "欢迎使用百度图片下载脚本！\n目前仅支持单个关键词。"
    print "下载结果保存在脚本目录下的results文件夹中。"
    print "=" * 50
    word = raw_input("请输入你要下载的图片关键词：\n")

    count = raw_input("请输入你要下载的图片的数目：\n")
    #创建保存图片的路径
    dirpath = mkDir("results")

    urls = buildUrls(word)
    index = 0
    flag = 1
    for url in urls:
        if flag == 2:
            break
        print "正在请求：", url
        html = requests.get(url, timeout=10).content.decode('utf-8')
        imgUrls = resolveImgUrl(html)
        if len(imgUrls) == 0:  # 没有图片则结束
            break
        for url in imgUrls:

            if downImg(url, dirpath, str(index) + ".jpg"):
                index += 1
                #print type(index),type(count)
                if index > int(count):
                    flag = 2
                    break
                print "已下载 %s 张" % index
    print u'开始执行选择图片程序'
    selectImg()
