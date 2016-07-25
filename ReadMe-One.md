爬取 One 上面的每日一图以及问答

## 一. 过程分析

![](http://7xrl8j.com1.z0.glb.clouddn.com/one1.png)

如上即为 One 首页。挺简单的,但是我们要批量抓取数据。只是简单的首页展示并不能满足。看网页源码如下:

![](http://ww2.sinaimg.cn/large/b10d1ea5jw1f61mz739aaj20s3061q58.jpg)

如网页源码所标注。目标应该就是我们的链接 url。我们将其复制进地址栏。果然验证猜想。另外几个圈起来的即为要抓取的字段。分别对应着:图片的 URL 地址,作者,日期,一句话简介。

![](http://7xrl8j.com1.z0.glb.clouddn.com/one3.png)

而当初我们就是要抓起批量的数据。所以这个 1406 就是我们首先要开刀。容易猜想出他就是历史内容。为验证,我们随机输入 1230 。果然如下所示。再多验证几次。大抵如是。所以我们抓取的时候,页面可以自己指定范围。当然会有 404 的时候。到时候我们也有解决的办法。

![](http://7xrl8j.com1.z0.glb.clouddn.com/one4.png)

One 的文章源码结构也是如上分析。道理亦然。

![](http://7xrl8j.com1.z0.glb.clouddn.com/one5.png)



## 二. 抓取代码

```python
def getContent(self,url):
    req = requests.get(url,headers=self.headers)
    if req.status_code == 200:
        oneImgs = OneImg()
        # 图片 URL
        pattern0 = re.compile('<div class="one-imagen">.*?<img src="(.*?)" alt="" />.*?</div>',re.S)
        imgItem = re.findall(pattern0, req.content)
        oneImgs.set('imgUrl',imgItem[0]).save()
        # 简介描述
        pattern1 = re.compile('<div class="one-cita">(.*?)</div>',re.S)
        intrItem = re.findall(pattern1, req.content)
        oneImgs.set('imgIntr', intrItem[0]).save()
        # 作者
        pattern2 = re.compile('<div class="one-imagen-leyenda">(.*?)</div>',re.S)
        authItem = re.findall(pattern2, req.content)
        replaceBR = re.compile('<br />')
        authItem = re.sub(replaceBR, "\n", authItem[0])
        oneImgs.set('imgAuth', authItem).save()
        # 日期
        pattern3 = re.compile('<p class="dom">(.*?)</p>.*?<p class="may">(.*?)</p>',re.S)
        timeItem = re.findall(pattern3, req.content)
        oneImgs.set('imgDate', timeItem[0][0]+timeItem[0][1]).save()
    else:
        print '这一页失败了'
```

核心代码如上。

* 采用 request 库来进行网络请求。一旦返回的 statusCode 不等于 200,就不会进行下一步动作。
* 采用正则来进行信息的过滤。当然 bs4 也是可以的。这里页面构造很简单,一会就写出来了。
* 对于抓取的数字内容含有 "<br/>",我们也可以采用正则过滤它,即用 "\n" 替代。

## 三. 数据存储

```python
class OneImg(Object):
    # imgUrl
    @property
    def imgUrl(self):
        return self.get('imgUrl')
    @imgUrl.setter
    def imgUrl(self, value):
        return self.set('imgUrl', value)
```

* 数据的存储为 leanCloud 云存储。这一块可以自己看看官方文档,非常简单。


* 如上代码。我们采用 property 属性来构建实体类。即面向对象思想的一些体现。这样存储过程就更为直观简单了。