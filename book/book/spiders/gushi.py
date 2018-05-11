# -*- coding: utf-8 -*-
from scrapy import Spider,Request
from book.items import BookItem
import scrapy

class GushiSpider(scrapy.Spider):
    name = 'gushi'
    # allowed_domains = ['https://so.gushiwen.org/gushi/tangshi.aspx']
    start_urls = ['https://so.gushiwen.org/gushi/tangshi.aspx/']

    def get_start_url(self, response):
        zhu_url = 'https://www.gushiwen.org/'
        all_url = response.css('.typecont span a::attr(href)')
        for tags in all_tags:
            a_url = tags.extract()
            url = zhu_url+a_url
            print(url)
            yield Request(url,callback=self.parse)
    def parse(self,response):
        item = BookItem()
        conent = response.css('div.sons:nth-child(2) > div:nth-child(1)')
        for con in conent:
            cen = con.css('head > meta:nth-child(5)::attr(content)').extract()
            name = con.css('div.sons:nth-child(2) > div:nth-child(1) > h1:nth-child(2)::text').extract()
            time = con.css('div.sons:nth-child(2) > div:nth-child(1) > p:nth-child(3) > a:nth-child(1)::text').extract()
            zuozhe = con.css('div.sons:nth-child(2) > div:nth-child(1) > p:nth-child(3) > a:nth-child(3)::text').extract()
            item['cen'] = cen
            item['name'] = name
            item['time'] = time
            item['zuozhe'] = zuozhe
            yield item



