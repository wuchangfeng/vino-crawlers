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
url = 'http://www.zhihu.com/question/31159026'
#多线程相关
FILE_LOCK = threading.Lock()
SHARE_Q = Queue.Queue()  #构造一个不限制大小的的队列
_WORKER_THREAD_NUM = 3  #设置线程的个数

class MyThread(threading.Thread) :

    def __init__(self, func) :
        super(MyThread, self).__init__()  #调用父类的构造函数
        self.func = func  #传入线程函数逻辑

    def run(self) :
        self.func()

class GetPic:
    url = None
    def __init__(self,url):
        self.url = url
        r = requests.get(self.url)
        self.soup = BeautifulSoup(r.content,"lxml")
        print r.status_code

    def getTitle(self):
         #replace() 将换行替换成空格
         title = self.soup.find("h2", class_="zm-item-title").string.replace("\n", "")
         return self

    def getAnsNums(self):
        answers_num = 0
        if self.soup.find("h3", id="zh-question-answer-num") != None:
            #可以参考这个源码，取出里面的字段。。。
            answers_num = int(self.soup.find("h3", id="zh-question-answer-num")["data-num"])
        print u"共有",answers_num,u"条回复"
        return answers_num

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
                            try:
                                urllib.urlretrieve(img_url,filename)
                            except Exception as e:
                                pass
                            img_counter += 1
                            print u"第%s"%img_counter,u"下载成功"

        return self
def worker() :
    global SHARE_Q
    while not SHARE_Q.empty():
        SHARE_Q.get() #获得任务
        #my_page = get_page(url)
        #find_title(my_page)  #获得当前页面的电影名
        #write_into_file(temp_data)
        time.sleep(1)
        SHARE_Q.task_done()
def main() :
    global SHARE_Q
    global getpic
    getpic = GetPic('http://www.zhihu.com/question/31159026')
    threads = []
    #douban_url = "http://movie.douban.com/top250?start={page}&filter=&type="
    #向队列中放入任务, 真正使用时, 应该设置为可持续的放入任务
    for index in xrange(10) :
        SHARE_Q.put(getpic.getAllImgs())
    for i in xrange(_WORKER_THREAD_NUM) :
        thread = MyThread(worker)
        thread.start()  #线程开始处理任务
        threads.append(thread)
    for thread in threads :
        thread.join()
    SHARE_Q.join()


if __name__ == '__main__':
    main()
#getpic = GetPic('http://www.zhihu.com/question/31159026')
#getpic.getTitle()
#getpic.getAnsNums()
#getpic.getAllImgs()

