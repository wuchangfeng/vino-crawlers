#-*- coding: utf-8 -*-
__author__ = 'Wu_cf'
'''
获得一个话题下面的所有答案
1:话题url
2:http://www.zhihu.com/topic/19575436/questions?page=1
  http://www.zhihu.com/topic/' + link_id + '/questions?page=' + str(i)'''
from auth import islogin
from auth import Logging
import requests,cookielib,sys,urllib,urllib2,os,json,re,threading,Queue,time
from bs4 import BeautifulSoup
basePath = r'F:\Catch_IMGS'
requests = requests.Session()
requests.cookies = cookielib.LWPCookieJar('cookies')
try:
    requests.cookies.load(ignore_discard=True)
except:
    print u"尚未登录知乎=="
if islogin() != True:
    print u"请重新登录=="
#字符编码设置
reload(sys)
sys.setdefaultencoding('utf8')

class GetTopics:
    def __init__(self,url):
        global pagehtml
        self.url = url
        r = requests.get(self.url)
        #print r.url
        self.soup = BeautifulSoup(r.content,"lxml")
        pagehtml = r.content
        #print r.content
        print r.status_code
    def test(self):
        testtitle = self.soup.find("title").string
        print testtitle
        return self
    def get_foucustopic_num(self):
        num = int(self.soup.find("span",class_="follow-topics-count").string)
        print u"关注了",num,u"个话题"
        return num
    def getAll_topic_link_name(self):
        answers_num = self.get_foucustopic_num()
        topic_counter = 0
        getallquestion = GetQuestions()
        for i in xrange((answers_num - 1) / 20 + 1):
                if i == 0:
                   print "=======",i
                   topic_items = re.findall(r'<a class="topic-item-title-link" href="/topic/(.*?)">(.*?)</a>', pagehtml, re.S)

                   for topic in topic_items:
                        link = topic[0]
                        name = topic[1]
                        #topic_num = topic_num +1
                        print link,name,topic_counter
                        topic_counter = topic_counter + 1
                        getallquestion.get_all_top_questions(name,link)
                else:
                    print '=======',i
                    post_url = "http://www.zhihu.com/topic"
                    urls = "http://www.zhihu.com/"
                    r = requests.get(urls)
                    results = re.compile(r"\<input\stype=\"hidden\"\sname=\"_xsrf\"\svalue=\"(\S+)\"", re.DOTALL).findall(r.text)
                    _xsrf = results[0]

                    page_num = i + 1

                    data = {
                        '_xsrf': _xsrf,
                        'page': page_num
                    }
                    header = {
                        'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",
                        'Host': "www.zhihu.com",
                        'Referer': self.url
                    }
                    r = requests.post(post_url, data=data, headers=header)

                    answer_list = r.json()["msg"]

                    for j in xrange(min(answers_num - i * 20, 20)):
                        topic_items = re.findall(r'<a class="topic-item-title-link" href="/topic/(.*?)">(.*?)</a>', answer_list[j], re.S)
                        for topic in topic_items:
                            link = topic[0]
                            name = topic[1]
                            print link,name,topic_counter
                            getallquestion.get_all_top_questions(name,link)
                            topic_counter = topic_counter + 1
        print topic_counter
        return self
class GetQuestions:
    '''1：根据话题来获得问题
       话题要不要存入进数据库或者其他什么方式
       3:http://www.zhihu.com/topic/19550523/top-answers?page=2
    '''
    def get_all_top_questions(self,name,link):
        #每隔话题爬10个页面吧
        question_num = 0
        default_url = 'http://www.zhihu.com/topic/' + link + '/top-answers'
        #question_url = 'http://www.zhihu.com/topic/' + link + '/top-answers?page=' + str(i)
        print u"话题为",name
        for i in xrange(10):

            if i == 0:
                print "=====页面",i
                try:
                    r = requests.get(default_url)
                except Exception as e:
                    pass
                question_items = re.findall(r'<h2><a class="question_link" target="_blank" href=(.*?)>(.*?)</a></h2>', r.content, re.S)
                for question in question_items:
                    question_num = question_num + 1
                    print question[1]," ",question_num

            else:
                print "=====页面",i
                changed_url = 'http://www.zhihu.com/topic/' + link + '/top-answers?page=' + str(i)
                try:
                    r = requests.get(changed_url)
                except Exception as e:
                    pass
                question_items = re.findall(r'<h2><a class="question_link" target="_blank" href=(.*?)>(.*?)</a></h2>', r.content, re.S)
                for question in question_items:
                    question_num = question_num + 1
                    print question[1]," ",question_num
def main():
   url = "http://www.zhihu.com/topic"
   gettopics = GetTopics(url)
   test = gettopics.test()
   gettopicsnum = gettopics.get_foucustopic_num()
   gettopicname = gettopics.getAll_topic_link_name()
if __name__ == '__main__':
    main()
