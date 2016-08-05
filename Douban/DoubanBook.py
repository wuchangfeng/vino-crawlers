# -*- coding:utf-8 -*-
import requests,re
from bs4 import BeautifulSoup
import leancloud
from leancloud import Object
import time

class Book:
    def __init__(self):
        leancloud.init("=====", "======")
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': self.user_agent}

    def getContent(self,url):
        reqContent = requests.get(url, headers=self.headers)
        if reqContent.status_code == 200:
            i = 0
            soup = BeautifulSoup(reqContent.content, 'html.parser')
            for link in soup.find_all('tr', 'item'):
                bookInfo = BookSave()
                print i
                try:
                    bookInfo.set('bookIntr',  self.getBookIntro(link.a['href'])).save()
                    bookInfo.set('imgUrl', link.find('a', 'nbg').contents[1]['src']).save()
                    bookInfo.set('bookTitle', link.find('div', 'pl2').a['title']).save()
                    bookInfo.set('bookAuth', link.find('p', 'pl').string).save()
                    bookInfo.set('bookRate', link.find('span', 'rating_nums').string).save()
                    bookInfo.set('rateNum', link.find('span', 'pl').string[1:-2].strip()).save()
                except leancloud.LeanCloudError as e:
                    print e.message
                i = i + 1
                '''
                print self.getBookIntro(link.a['href'])
                print link.find('a', 'nbg').contents[1]['src']
                print link.find('div', 'pl2').a['title']
                print link.find('p', 'pl').string
                print link.find('span', 'rating_nums').string
                print link.find('span', 'pl').string[1:-2].strip()
                '''

    def getBookIntro(self, url):
        intrContent = requests.get(url, headers=self.headers)
        if intrContent.status_code == 200:
            pattern4 = re.compile('<div class="">.*?<style .*?>.*?</style>.*?<div .*?>(.*?)</div>', re.S)
            BookIntro = re.findall(pattern4, intrContent.content)
            if(len(BookIntro) > 0):
                bookInfro = BookIntro[0].strip().decode('utf-8').replace('<p>',' ').replace('</p>',' ')
            else:
                print 'data error'
            if(len(bookInfro) > 0):
                return bookInfro
            else:
                print 'no data'
    def start(self):
        for page in range(5,10):
            if(page == 0):
                baseUrl = 'https://book.douban.com/top250'
                self.getContent(baseUrl)
                print 'page 1 ok'
            else:
                baseUrl = 'https://book.douban.com/top250?start='
                pages = page * 25
                url = baseUrl + str(pages)
                self.getContent(url)
                time.sleep(5)
                print 'page', page, 'ok'


class BookSave(Object):
    # bookimgurl
    @property
    def imgUrl(self):
        return self.get('imgUrl')
    @imgUrl.setter
    def imgUrl(self, value):
        return self.set('imgUrl', value)

    # bookIntr
    @property
    def bookIntr(self):
        return self.get('bookIntr')
    @bookIntr.setter
    def bookIntr(self, value):
        return self.set('bookIntr', value)

    # bookTitle
    @property
    def bookTitle(self):
        return self.get('bookTitle')
    @bookTitle.setter
    def bookTitle(self, value):
        return self.set('bookTitle', value)

    # bookAuth
    @property
    def bookAuth(self):
        return self.get('bookAuth')
    @bookAuth.setter
    def bookAuth(self, value):
        return self.set('bookAuth', value)

    # bookRate
    @property
    def bookRate(self):
        return self.get('bookRate')
    @bookRate.setter
    def bookRate(self, value):
        return self.set('bookRate', value)

    # rateNum
    @property
    def rateNum(self):
        return self.get('rateNum')
    @rateNum.setter
    def rateNum(self, value):
        return self.set('rateNum', value)



book = Book()
book.start()
