
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import urllib
import requests,re,time
import pymongo
import simplejson as json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class lagouCrawler:

    def __init__(self):
        global collection
        global db
        client = pymongo.MongoClient("localhost", 27017)
        db = client.lagouDB


    def search_data(self):
        #db.LaGouCollection.drop()
        print db.Collection.count()
        db.Collection.drop()
        '''
        cursor = db.LaGouCollection.find({"positionName": "Ruby"})
        for document in cursor:
            print document
        '''
    def insert_data(self,data):

        db.Collection.insert_one(data)
        print u'一共',db.Collection.count(),u'条数据了'




    def get_data(self,url,pageNum,keyWord):
        page_headers = {
            'Host': 'www.lagou.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
            'Connection': 'keep-alive'
        }
        play_load = {'first': 'true', 'pn': pageNum, 'kd': keyWord}
        req = requests.post(url, headers=page_headers, params=play_load)
        if req.json()['content']['pageNo'] == 0:
            flag = True
            return flag
        if req.status_code == 200:
            req = req.json()
            if (('content' in req)):
                list_con = req['content']['positionResult']['result']
                if len(list_con) >= 0:

                    for i in list_con:
                        formatData = {
                            "companyShortName": i['companyShortName'],
                            "salary":i['salary'],
                            "city": i['city'],
                            "education": i['education'],
                            "positionName": i['positionName'],
                            "workYear": i['workYear'],
                            "companySize": i['companySize'],
                            "financeStage": i['financeStage'],
                            "industryField": i['industryField']
                        }
                        lagouCrawler.insert_data(formatData)
            else:
                print u'数据错误',req
        else:
            print u'网络不好'


    def start(self):

        for i in city:
            print u'当前城市是：',i
            word = urllib.quote(i)
            url = 'http://www.lagou.com/jobs/positionAjax.json?px=default&city={city}&needAddtionalResult=false'
            url = url.format(city=word)
            for positionItem in position:
                print u'当前职位是：', positionItem
                for page in xrange(1, 31):
                    print u'当前抓取页面是：', page
                    time.sleep(3)
                    infoItem = lagouCrawler.get_data(url, page, positionItem)
                    if infoItem == True:
                        break
        print u'抓取完毕。'

    '''
    def start(self,url):

        for positionItem in position:
            print u'当前职位是：', positionItem
            for page in xrange(1, 31):
                print u'当前抓取页面是：', page
                time.sleep(4)
                infoItem = lagouCrawler.get_data(url, page, positionItem)
                if infoItem == True:
                    break
        print u'抓取完毕。一共存储了', infoItem, u'条数据'

    '''


if __name__ == '__main__':
    count = 0
    position = [
    '数据挖掘', 'Java','Python','PHP','.NET','C#','C++','C','VB','Perl','Ruby','Hadoop','Node.js','Go',
    'ASP', 'Shell','自然语言处理', '搜索推荐', '精准推荐', 'HTML5', 'Android', '技术经理', '架构师', '测试', '技术总监',
    'IOS','JavaScript', '测试工程师','网络工程师','UI','UE','数据分析','MongoDB','MySql','SQLServer','Oracle',
                '运维工程师','病毒分析','WEB安全','网络安全']
    city = ['北京', '上海', '深圳', '广州', '杭州', '成都', '南京', '武汉', '西安', '厦门', '长沙', '苏州', '天津',
            '重庆', '郑州', '青岛', '合肥', '福州', '济南', '大连', '珠海', '无锡', '佛山','东莞', '宁波','中山']
    lagouCrawler = lagouCrawler()
    #url = lagouCrawler.get_url()
    #lagouCrawler.search_data()
    lagouCrawler.start()

