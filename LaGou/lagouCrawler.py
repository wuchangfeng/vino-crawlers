# -*- coding:utf-8 -*-
import urllib,datetime
import requests,re,time
import pymongo
import time,threading
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

    def insert_data(self,data):

        data['_id'] = data['positionId']
        data['updateTime'] = datetime.datetime.now()
        # 防止重复插入
        db.Collection.update_one(
            filter={'_id': data['_id']},
            update={'$set': data},
            upsert=True
        )
        count = db.Collection.count()
        print u'已经存储了：',count,u'条记录'


    def get_data(self,url,pageNum,keyWord):

        page_headers = {
            'Host': 'www.lagou.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
            'Connection': 'keep-alive'
        }
        # 构建表单
        play_load = {'first': 'false', 'pn': pageNum, 'kd': keyWord}
        # 代理容易失效,自己替换
        proxies = {
            "http": "http://42.159.251.84:41795",
            "http": "http://121.33.226.167:3128",
            'http': 'http://121.61.96.241:8118',
            'http': 'http://39.1.46.165:8080'
        }
        # requests 请求
        req = requests.post(url, headers=page_headers, params=play_load)
        # 如果 pageNo == 0 表示后面没有页数了，不用继续往后面请求了
        if req.json()['content']['pageNo'] == 0:
            flag = True
            return flag

        # 如果 status_code == 200 表示请求正常
        if req.status_code == 200:
            req = req.json()

            if (('content' in req)):
                list_con = req['content']['positionResult']['result']
                if len(list_con) >= 0:
                    for i in list_con:
                        # 构建存储字段
                        formatData = {
                            "companyShortName": i['companyShortName'],
                            "salary":i['salary'],
                            "city": i['city'],
                            "education": i['education'],
                            "positionName": i['positionName'],
                            "workYear": i['workYear'],
                            "companySize": i['companySize'],
                            "financeStage": i['financeStage'],
                            "industryField": i['industryField'],
                            "positionId":i['positionId']
                        }

                        lagouCrawler.insert_data(formatData)

            else:
                print u'数据错误：',req

        else:
            print u'网络不好,返回状态码：',req.status_code

    def start(self):

        for hy in hangye:
            print u'当前行业是：', hy
            # 中文字符转换成16进制
            keyWord1 = urllib.quote(hy)
            for i in citys:
                print u'当前城市是：',i
                keyWord2 = urllib.quote(i)
                url = 'http://www.lagou.com/jobs/positionAjax.json?hy={hy}&px=default&city={city}&needAddtionalResult=false'
                url = url.format(hy=keyWord1,city=keyWord2)
                for positionItem in positions:
                    print u'当前职位是：', positionItem
                    for page in xrange(1, 31):
                        print u'当前抓取页面是：', page
                        time.sleep(10)
                        infoItem = lagouCrawler.get_data(url, page, positionItem)
                        if infoItem == True:
                            break
        print u'抓取完毕。'

if __name__ == '__main__':

    count = 0

    # 职位
    positions = ['HTML5', 'Android', 'Python', 'PHP','.NET', 'C#', 'C++', 'C', 'VB', 'Perl', 'Ruby', 'Hadoop', 'Node.js', 'Go',
        'ASP', 'Shell', '自然语言处理', '搜索推荐', '精准推荐','技术经理', '架构师', '测试', '技术总监',
        'IOS', 'JavaScript', '网络工程师', 'UI', 'UE', '数据分析', 'MongoDB', 'MySql', 'SQLServer', 'Oracle',
        '运维工程师', 'WEB安全', '网络安全','数据挖掘', 'Java','爬虫工程师']

    # 城市
    citys = ['北京', '上海', '深圳', '广州', '杭州', '成都', '南京', '武汉', '西安', '厦门', '长沙', '苏州', '天津',
             '重庆', '合肥', '济南', '大连', '珠海', '宁波', '中山']

    # 行业
    hangye = ['教育','文化娱乐','移动互联网','游戏','O2O','硬件','社交网络','旅游',' 医疗健康','生活服务','信息安全',' 数据服务','广告营销','分类信息','电子商务','金融','企业服务',]

    lagouCrawler = lagouCrawler()
    lagouCrawler.start()

