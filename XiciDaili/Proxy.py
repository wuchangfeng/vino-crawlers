# -*- coding=utf-8 -*-
__author__ = 'Rocky'
import urllib2, time, datetime
from lxml import etree
import pymongo
import sqlite3,time,requests

class getProxy():

    def __init__(self):
        self.user_agent = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
        self.header = {"User-Agent": self.user_agent}
        self.dbname="proxy.db"
        self.now = time.strftime("%Y-%m-%d")
        global collection
        global db
        client = pymongo.MongoClient("localhost", 27017)
        db = client.lagouDB

    def insertDB(self,data):
        db.IP.insert_one(data)
        print 'save ok'

    def getContent(self, num):
        nn_url = "http://www.xicidaili.com/nn/" + str(num)
        #国内高匿
        req = urllib2.Request(nn_url, headers=self.header)
        resp = urllib2.urlopen(req, timeout=10)
        content = resp.read()
        et = etree.HTML(content)
        result_even = et.xpath('//tr[@class=""]')
        result_odd = et.xpath('//tr[@class="odd"]')

        for i in result_even:
            t1 = i.xpath("./td/text()")[:2]
            p = "http"+":"+"//"+t1[0]+":"+t1[1]
            formatData = {
                "proxy": p
            }

            # 先验证是否有用
            if obj.test_useful(p):
                print p
                #obj.insertDB(formatData)
                '''
                with open(path, 'a') as f:
                    f.write(p + '\n')
                '''

        for i in result_odd:
            t2 = i.xpath("./td/text()")[:2]
            p = "http" + ":" + "//" + t2[0] + ":" + t2[1]
            formatData = {
                "proxy": p
            }

            # 先验证是否有用
            if obj.test_useful(p):
                print p
                #obj.insertDB(formatData)


    def test_useful(self,proxy):
        try:
            proxies = {'http': proxy}
            print proxies
            r = requests.get('http://www.baidu.com',proxies=proxies)
            if r.status_code == 200:
                print 'Successfully get one'
            return True
        except Exception, e:
            print e
            return False

    def getProxies(self):
        print db.IP.count()
        cur = db.IP.find()
        for i in cur:
            print i


    def loop(self,page):
        for i in range(1,page):
            self.getContent(i)


if __name__ == "__main__":
    path = 'mt_proxy.txt'
    now = datetime.datetime.now()
    print "Start at %s" % now
    obj=getProxy()
    obj.loop(5)
    #b = obj.getProxies()
    #obj.test_useful(b)


