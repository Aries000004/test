# -*- coding: utf-8 -*-
import scrapy
from xiecheng.items import XiechengItem

class XieSpider(scrapy.Spider):
    name = 'xie'
    allowed_domains = ['you.ctrip.com']
    start_urls = ['http://you.ctrip.com/searchsite/?query=杭州']

    def parse(self, response):
        item = XiechengItem()
        da = response.xpath('//li[@class="cf"]')
        for xiao in da:
            Destination = xiao.xpath('./dl/dt/a[1]/text()').extract()
            Destination_url = xiao.xpath('./dl/dt/a[1]/@href').extract()
            print(Destination)
            print(Destination_url)




