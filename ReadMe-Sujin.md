抓取素锦网站上文章

## 1. 步骤分析

如下两张图片既是网站主要布局结构,我们要抓取的数据也是一目了然。

![](http://7xrl8j.com1.z0.glb.clouddn.com/Sujin1.png)

![](http://7xrl8j.com1.z0.glb.clouddn.com/sunjin2.png)

拖动页面。可以看到加载更多按钮。但是地址栏没有变化。点击 F12 调试模式。如 2 所示看见 http//isujin.com/page/3。容易猜想输入 n(n 正常合理范围之内) 也是可以获得数据的。并且如果返回数据成功,返回 statusCode == 200。这个状态码对我们非常有用。

![](http://7xrl8j.com1.z0.glb.clouddn.com/sujin3.png)

点击页面,查看源码,红框内即为要爬取的字段内容。

![](http://7xrl8j.com1.z0.glb.clouddn.com/sujin4.png)

## 2.  抓取代码

抓取的核心代码如下所示,数据的过滤收集采用的 BeautifulSoup4 这个库。很简单。

```python
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
```
## 3. 存储代码

存储过程很简单。存储在 leancloud 云端。用 leanCloud 官方提供的 python sdk 来进行数据的存储工作。部分代码如下:

```python
@property
def title(self):
    return self.get('title')
@title.setter
def title(self, value):
    return self.set('title', value)
```