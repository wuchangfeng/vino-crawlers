##  [落网]

* 落网的音乐逼格真的很高，都是自己喜欢的民谣类型，故爬虫抓取之。强烈推荐大家去欣赏落网的音乐，如果有兴趣也可以知乎一下落网的历史。真的非常不错。

### 说明
* 整个网站还是很简单的，没有模拟登陆，验证码啥的，甚至请求头都不用写。爬虫也没有写的太暴力，"温柔"的爬取,为此加了延时，另一方面也是怕被识别出是机器。

### 准备
* 工具：python 2.7,PyCharm
* 类库：Requests,BeautifulSoup,os

### 分析
* 进入落网官网，发现如下图所示,其中804(可以自己输入相应期刊)就是期刊，每一期都有十左右首音乐。

![](http://7xrl8j.com1.z0.glb.clouddn.com/%E6%AF%8F%E4%B8%80%E6%9C%9F%E6%AD%8C%E5%8D%95.jpg)

* 点击页面进入HTML元素页面，可以看见歌曲名字，专辑名，歌者，但是怎么没有歌曲资源的url？

![](http://7xrl8j.com1.z0.glb.clouddn.com/%E6%AD%8C%E6%9B%B2%E5%90%8D%E5%AD%97.jpg)

* 没有歌曲的url我们就不能下载，那么我们要看看我们每一次换歌曲，发生了什么请求，点击审查元素，如下结果。

![](http://7xrl8j.com1.z0.glb.clouddn.com/%E6%AD%8C%E6%9B%B2url.jpg)

* 如上图所示一个Request url，我们复制进浏览器地址输入栏，发现如下所示，没错这就是我们下载的url了。

![](http://7xrl8j.com1.z0.glb.clouddn.com/%E6%AD%8C%E6%9B%B2.jpg)

### 开始

* 开始之前我们要获取歌曲相应的信息，我们采用bs这个库来解析HTML元素。
* 我们采用Requests来进行网络请求与下载，下载音乐就要用到稍微逼格高一点的用法了，我们下载它的响应流文件。
* 具体用法见[Requests响应体内容工作流](http://cn.python-requests.org/en/latest/user/advanced.html)

### 总结
* 抓取还是比较简单的,只用到了基本的requests和beautifulsoup,只是很难想到要流式读取响应头，这是requests的高级用法。
* 我们抓取的目的就是把歌曲下载到本地，自由不用联网的听，速度个人感觉不要太追求，不要坑人家服务器啊。

### 参考

* [落网爬虫](https://github.com/shuson/luooder.git)

### 结果

![](http://7xrl8j.com1.z0.glb.clouddn.com/%E7%BB%93%E6%9E%9C.jpg)

### 感谢

* [TZS](https://github.com/1041218129)
* [DLX4](https://github.com/DLX4)
