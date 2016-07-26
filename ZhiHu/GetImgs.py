#-*- coding: utf-8 -*-
__author__ = 'Wu_cf'
from auth import islogin
from auth import Logging
import requests,cookielib,sys,urllib,urllib2,os,json,re
from bs4 import BeautifulSoup
basePath = r'F:\SPIDER_IMGS'
requests = requests.Session()
requests.cookies = cookielib.LWPCookieJar('cookies')

try:
    requests.cookies.load(ignore_discard=True)
except:
    Logging.error(u"你还没有登录知乎哦 ...")
    Logging.info(u"执行 `python auth.py` 即可以完成登录。")
    raise Exception("无权限(403)")
if islogin() != True:
    Logging.error(u"你的身份信息已经失效，请重新生成身份信息( `python auth.py` )。")
    raise Exception("无权限(403)")
reload(sys)
sys.setdefaultencoding('utf8')
url = 'http://www.zhihu.com/question/31159026'
'''
图片获取类
'''
class GetPic:
    url = None
    def __init__(self,url):
        self.url = url
        r = requests.get(self.url)
        self.soup = BeautifulSoup(r.content,"lxml")
        print r.status_code
    '''
    获取中文标题
    '''
    def getTitle(self):
         #replace() 将换行替换成空格
         title = self.soup.find("h2", class_="zm-item-title").string.replace("\n", "")
         return self
    '''
    获取答案数量,这个很重要，图片(图片url)就包含在答案中，
    '''
    def getAnsNums(self):
        answers_num = 0
        if self.soup.find("h3", id="zh-question-answer-num") != None:
            #可以参考这个源码，取出里面的字段。。。
            answers_num = int(self.soup.find("h3", id="zh-question-answer-num")["data-num"])
        print u"共有",answers_num,u"条回复"
        return answers_num
    '''
    下载图片,这里可能写的有点乱.注明一下：1：首先我们在还未点击加载更多时候，提取图片，即 if i== 0阶段
    2：在我们点击了加载更多时候，提取图片（我们可以在点击加载更多时候，看看浏览器发送了什么内容）
    3:具体的可以看http://lovenight.github.io这里的博客，写的非常详细，具体实现肯呢个不一样，但是思路都是一样的
    '''
    def getAllImgs(self):
        answers_num = self.getAnsNums()
        img_counter = 0
        for i in xrange((answers_num - 1) / 50 + 1):
                if i == 0:
                    img_list = self.soup.find_all("img", class_="origin_image zh-lightbox-thumb lazy")
                    for img in img_list:
                         img_url = img["data-original"]
                         picname = str(img_counter) + '.jpg'
                         filename = os.path.join(basePath,picname)
                         urllib.urlretrieve(img_url,filename)
                         img_counter += 1
                         print u"第%s"%img_counter,u"下载成功"
                else:
                    print u"===第",i,u"次xrf请求"
                    post_url = "http://www.zhihu.com/node/QuestionAnswerListV2"
                    urls = "http://www.zhihu.com/"
                    r = requests.get(urls)
                    results = re.compile(r"\<input\stype=\"hidden\"\sname=\"_xsrf\"\svalue=\"(\S+)\"", re.DOTALL).findall(r.text)
                    _xsrf = results[0]
                    offset = i * 50
                    params = json.dumps(
                        {"url_token": int(self.url[-8:-1] + self.url[-1]), "pagesize": 50, "offset": offset})
                    data = {
                        '_xsrf': _xsrf,
                        'method': "next",
                        'params': params
                    }
                    header = {
                        'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",
                        'Host': "www.zhihu.com",
                        'Referer': self.url
                    }
                    r = requests.post(post_url, data=data, headers=header)

                    answer_list = r.json()["msg"]
                    for j in xrange(min(answers_num - i * 50, 50)):
                        answer_soup = BeautifulSoup(answer_list[j],"lxml")
                        img_list = answer_soup.find_all("img", class_="origin_image zh-lightbox-thumb lazy")
                        for img in img_list:
                            img_url = img["data-original"]
                            picname = str(img_counter) + '.jpg'
                            filename = os.path.join(basePath,picname)
                            urllib.urlretrieve(img_url,filename)
                            img_counter += 1
                            print u"第%s"%img_counter,u"下载成功"
        return self
      
#问题连接，以及启动程序  
getpic = GetPic('http://www.zhihu.com/question/31159026')
getpic.getTitle()
getpic.getAnsNums()
getpic.getAllImgs()

