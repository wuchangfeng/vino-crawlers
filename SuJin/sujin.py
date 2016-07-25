# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests,re,time
import leancloud
from leancloud import Object


'''
爬虫类,用来从 Sujin 上抓取图片,文章,以及一些信息
'''
class SuJin:
    def __init__(self):
        leancloud.init("xxxx", "xxxx")
        self.pageIndex = 1
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': self.user_agent}

    def getPage(self, pageIndex):
        url = 'http://isujin.com/page/' + str(pageIndex)
        req = requests.get(url, headers=self.headers)
        return req

    def getItem(self,pageIndex):
        req = self.getPage(pageIndex)
        if req.status_code == 200:
            print '第',pageIndex,'页ok'
            soup = BeautifulSoup(req.content, 'html.parser')
            for link in soup.find_all('div', 'post'):
                sjContent = Content()
                sjContent.set("title", link.a['title']).save()
                sjContent.set("detail", self.getContent(link.a['href'])).save()
                sjContent.set("ids", link.a['data-id']).save()
                sjContent.set("img", link.a.contents[1]['src']).save()
                sjContent.set("intr", soup.find_all('p')[1].string).save()

    def getContent(self,contentUrl):
        string = ''
        reqContent = requests.get(contentUrl)
        contentSoup = BeautifulSoup(reqContent.content, 'html.parser')
        for s in contentSoup.find('div', 'content').p.stripped_strings:
            string = string + s + '\n'
        return string

    def start(self):
        nowPage = 1
        while nowPage <= 10:
            nowPage += 1
            time.sleep(4)
            self.getItem(nowPage)

'''
实体类,用来将信息存储在 leancloud
'''
class Content(Object):
    @property
    def title(self):
        return self.get('title')
    @title.setter
    def title(self, value):
        return self.set('title', value)

    @property
    def detail(self):
        return self.get('detail')
    @detail.setter
    def detail(self, value):
        return self.set('detail', value)

    @property
    def ids(self):
        return self.get('ids')
    @ids.setter
    def ids(self, value):
        return self.set('ids', value)

    @property
    def img(self):
        return self.get('img')
    @img.setter
    def img(self, value):
        return self.set('img', value)

    @property
    def intr(self):
        return self.get('intr')
    @intr.setter
    def intr(self, value):
        return self.set('intr', value)


spider = SuJin()
spider.start()
