# -*- coding: utf-8 -*-
'''
汉沽租房信息，来自安居客，存入mongdb
'''
from scrapy.spider import Spider
from zufang.items import ZufangItem
from scrapy import Request
class FangSpider(Spider):
    name = 'fang'
    # allowed_domains = ['http://zu.tj.fang.com/']
    start_urls = ['https://tj.zu.anjuke.com/fangyuan/hangutianjin/&utm_term=%E7%A7%9F%E6%88%BF/']
    def parse(self, response):
        item = ZufangItem()
        #注意div的位置，优先查看源码
        dakuangjia = response.xpath('//div[@class="zu-itemmod  "]')
        for xiaokuangjia in dakuangjia:
            title = xiaokuangjia.xpath('./div[@class="zu-info"]/h3/a/text()').extract()
            size = xiaokuangjia.xpath('./div[@class="zu-info"]/p[1]/text()').extract()
            price = xiaokuangjia.xpath('./div[@class="zu-side"]/p/strong/text()').extract()
            place = xiaokuangjia.xpath('./div[@class="zu-info"]/address/text()').extract()
            item['title'] = title
            try:
                item['size'] = size[1]
            except IndexError:
                print('')
            item['price'] = price
            item['place'] = place[1].replace('  ','').replace('\xa0\xa0\n','')#用replace()函数去除空格和换行
            yield item
        # prices = response.xpath('//div[@class="zu-side"]/p/strong/text()').extract()
        # for price in prices:
        #     item['price']=price
        #     yield item


        # next_page = response.xpath('//div[@class="fanye"]/a[contains(text(),"下一页")]/@href').extract_first()
        next_page_url = response.xpath('//a[@class="aNxt"]/@href').extract_first()
        if next_page_url:
            # print(next_page_url)
            yield Request(next_page_url,callback=self.parse)


