# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests,re
import leancloud
from leancloud import Object
import time

'''
爬虫类,用来从 one 上抓取图片,问题以及回答
'''
class One:
    def __init__(self):
        leancloud.init("xxxx", "xxxx")
        self.pageIndex = 1
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': self.user_agent}

    def getContent(self,url):
        req = requests.get(url,headers=self.headers)
        if req.status_code == 200:
            oneImgs = OneImg()
            # 图片 URL
            pattern0 = re.compile('<div class="one-imagen">.*?<img src="(.*?)" alt="" />.*?</div>',re.S)
            imgItem = re.findall(pattern0, req.content)
            oneImgs.set('imgUrl',imgItem[0]).save()
            # 简介描述
            pattern1 = re.compile('<div class="one-cita">(.*?)</div>',re.S)
            intrItem = re.findall(pattern1, req.content)
            oneImgs.set('imgIntr', intrItem[0]).save()
            # 作者
            pattern2 = re.compile('<div class="one-imagen-leyenda">(.*?)</div>',re.S)
            authItem = re.findall(pattern2, req.content)
            replaceBR = re.compile('<br />')
            authItem = re.sub(replaceBR, "\n", authItem[0])
            oneImgs.set('imgAuth', authItem).save()
            # 日期
            pattern3 = re.compile('<p class="dom">(.*?)</p>.*?<p class="may">(.*?)</p>',re.S)
            timeItem = re.findall(pattern3, req.content)
            oneImgs.set('imgDate', timeItem[0][0]+timeItem[0][1]).save()
        else:
            print '这一页失败了'


    def getQA(self,url):
        reqContent = requests.get(url,headers=self.headers)
        if reqContent.status_code == 200:
            oneQa = OneQa()
            # 获取问题以及简介
            pattern = re.compile(
                '<div class="cuestion-q-icono">.*?</div>.*?<h4>(.*?)</h4>.*?<div class="cuestion-contenido">(.*?)</div>', re.S)
            questionTtems = re.findall(pattern, reqContent.content)
            for questionTtem in questionTtems:
                oneQa.set('qaIntr',questionTtem[0]).save()
                oneQa.set('qaDetail',questionTtem[1]).save()
            # 获取回答
            pattern2 = re.compile(
                '<div class="cuestion-a-icono">.*?</div>.*?<h4>(.*?)</h4>.*?<div class="cuestion-contenido">(.*?)</div>', re.S)
            answerItems = re.findall(pattern2, reqContent.content)
            for answerItem in answerItems:
                replaceBR = re.compile('<br>')
                answer = re.sub(replaceBR, "\n", answerItem[1])
                oneQa.set('qaAnsw', answer).save()
        else:
            print '这一页失败了'

    def start(self):
        baseUrl = 'http://wufazhuce.com/question/'
        baseUrl1 = 'http://wufazhuce.com/one/'
        for pageNum in range(1350,1410):
             print '第',pageNum,'页ok'
             url = baseUrl + str(pageNum)
             url1 = baseUrl1 + str(pageNum)
             time.sleep(6)
             self.getQA(url)
             self.getContent(url1)

'''
实体类用来存储到 Leancloud
'''
class OneImg(Object):
    # imgUrl
    @property
    def imgUrl(self):
        return self.get('imgUrl')
    @imgUrl.setter
    def imgUrl(self, value):
        return self.set('imgUrl', value)
    # imgIntr
    @property
    def imgIntr(self):
        return self.get('imgIntr')
    @imgIntr.setter
    def imgIntr(self, value):
        return self.set('imgIntr', value)
    # imgAuth
    @property
    def imgAuth(self):
        return self.get('imgAuth')
    @imgAuth.setter
    def imgAuth(self, value):
        return self.set('imgAuth', value)
    # imgDate
    @property
    def imgDate(self):
        return self.get('imgDate')
    @imgDate.setter
    def imgDate(self, value):
        return self.set('imgDate', value)

class OneQa(Object):
    # qaIntr
    @property
    def qaIntr(self):
        return self.get('qaIntr')
    @qaIntr.setter
    def qaIntr(self, value):
        return self.set('qaIntr', value)
    # qaDetail
    @property
    def qaDetail(self):
        return self.get('qaDetail')
    @qaDetail.setter
    def qaDetail(self, value):
        return self.set('qaDetail', value)
    # qaAnsw
    @property
    def qaAnsw(self):
        return self.get('qaAnsw')
    @qaAnsw.setter
    def qaAnsw(self, value):
        return self.set('qaAnsw', value)


one = One()
one.start()




