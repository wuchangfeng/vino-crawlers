# -*- coding: utf-8 -*-
from scrapy.selector import Selector
import scrapy
from scrapy.contrib.loader import ItemLoader, Identity
from fun.items import MeizituItem


class MeizituSpider(scrapy.Spider):
    name = "meizitu"
    allowed_domains = ["meizitu.com"]
    # 首页访问URL
    start_urls = (
        'http://www.meizitu.com/',
    )
    
    def parse(self, response):
        sel = Selector(response)
        for link in sel.xpath('//h2/a/@href').extract():
            request = scrapy.Request(link, callback=self.parse_item)
            yield request
        
        # 获取之后访问URL
        pages = sel.xpath("//div[@class='navigation']/div[@id='wp_page_numbers']/ul/li/a/@href").extract()
        print('pages: %s' % pages)
        if len(pages) > 2:
            # 下一个页面的URl 
            page_link = pages[-2]
            page_link = page_link.replace('/a/', '')
            request = scrapy.Request('http://www.meizitu.com/a/%s' % page_link, callback=self.parse)
            yield request

    # 解析URL获得下载图片URL
    def parse_item(self, response):
        # 解析http://www.meizitu.com/a/5336.html获取图片URL
        l = ItemLoader(item=MeizituItem(), response=response)
        l.add_xpath('image_urls', "//div[@id='picture']/p/img/@src", Identity())
        l.add_value('url', response.url)
        return l.load_item()