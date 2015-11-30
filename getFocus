#-*- coding: utf-8 -*-
__author__ = 'Wu_cf'
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
'''
1:每一个用户都有一个hash_id应该是其用户标志，可以在chorme浏览器看得到这个，然后在html页面全局搜索即可用正则获得该值
2：可以在批量获得某个话题下面的用户，但是获得大量关注者那个 start参数还是没搞清楚什么意思
3：更换话题，假如想关注NBA底下的所有用户，需要首先获得nba这个话题的link-id
4:start关键字这么来的 t = int(time.time()) 十位数的时间戳
'''
topic_url = 'http://www.zhihu.com/topic/19556945/followers'
def getMessage():
    r = requests.get(topic_url)
    raw_xsrf = re.findall('xsrf(.*)', r.text)
    _xsrf = raw_xsrf[0][9:-3]
    return _xsrf
#得到hash_id
def getHash():
    global header_info
    hash_id_all = []
    post_url = topic_url
    xsrf = getMessage()
    header_info = {
    "Accept":"*/*",
    "Accept-Encoding":"gzip,deflate,sdch",
    "Accept-Language":"zh-CN,zh;q=0.8",
    "Connection":"keep-alive",
    "Content-Length":"127",
    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
    "DNT":"1",
    "Host":"www.zhihu.com",
    "Origin":"http://www.zhihu.com",
    "Referer":topic_url,
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "X-Requested-With":"XMLHttpRequest",
    }
    for i in range(15):
         x = 0 + i * 20
         start = int(time.time())
         payload={"offset":x, "start":start, "_xsrf":xsrf,}
        # time.sleep(3)
         result = requests.get(post_url, data=payload, headers=header_info)
         #print result.text
         raw_hash_id = re.findall('<a href=.*? name=.*? class=.*? id=(.*?)>.*?</a>', result.text)
         for item in raw_hash_id:
             if item[4:36] > 32:
               hash_id_all.append(item[4:36])
         print "get hash_id",i,"success!"
    return hash_id_all
def getFocus():
    hash_id = getHash()
    xsrf = getMessage()
    i = 0
    for x in hash_id:
        i = i + 1
        params = json.dumps({"hash_id":x})
        payload={"method":"follow_member", "params":params, "_xsrf":xsrf,}
        click_url = 'http://www.zhihu.com/node/MemberFollowBaseV2'
        try:
            result = requests.post(click_url, data=payload, headers=header_info)
        except Exception as e:
            print u"不能关注了"

        if result.status_code == 200:
            print u"关注成功"," ",i
        else:
            print u"fucking"
    print u"就这么多了！！！！"

def main():
   #getHash()
   getFocus()
if __name__ == '__main__':
    main()
