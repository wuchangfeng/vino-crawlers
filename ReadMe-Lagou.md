### 思路

* 开始即根据职位来抓取相应的招聘职位数量。但是只有 1w 多。数量不达标。
* 组合关键字抓取。如组合城市,职位,服务领域。即可达成抓取 5w 数量目标。

### 细节

如下 Request URL 中的 %E7... 即为对应查询关键字的 16 进制表现形式。

![](http://ww1.sinaimg.cn/large/b10d1ea5gw1f6un014yqij20j7033wet.jpg)

如下 Form Data 皆为 Post 需要构建的表单。

![](http://ww2.sinaimg.cn/large/b10d1ea5gw1f6un0gaislj20ja04ldfz.jpg)

### 存储

* 为保证存储和查询速度。选择 MongoDB 数据库。
* 为保证插入不重复。对插入语句进行优化。

```python
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
```