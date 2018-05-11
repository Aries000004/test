'''
存入数据库会顺序混乱
'''
import scrapy
from scrapy import Spider,Request
import json
from taobao.items import TaobaoItem
import re
class Taobao(Spider):
    name = 'tao'
    keyword = '笔记本电脑'
    count=0
    #适用于淘宝页面（天猫要更改url）
    start_url = 'https://s.taobao.com/search?q={keyword}&s={i}'
    url = 'https://s.taobao.com/search?spm=a230r.1.0.0.85cb57e1ftkM73&q={keyword}&spu_title={title}' \
       '&app=detailproduct&pspuid={id}&cat=1101&from_pos={from_pos}&spu_style=grid'

    def start_requests(self):
        for i in range(0, 15):
            yield Request(self.start_url.format(keyword=self.keyword,i=str(i*48)),callback=self.parse)
    def parse(self, response):
        item = TaobaoItem()
        pattern = re.compile(r',"price":"(.*?)","trace":', re.S)
        price = re.findall(pattern, response.text)
        pattern = re.compile(r',"title":"(.*?)","pic_url":', re.S)
        title = re.findall(pattern, response.text)
        pattern = re.compile(r',"month_sales":"(.*?)","seller":', re.S)
        month_sales = re.findall(pattern, response.text)
        pattern = re.compile(r'"20_1101.default_0_\d+_\d{7}"', re.S)
        shujus = re.findall(pattern, response.text)
        for x in range(0, len(title)):
            # print(x)
            item['price'] = price[x]  # 价格
            item['title'] = title[x]  # 名称
            item['month_sales'] = month_sales[x]  # 月成交量
            # print(item)
            pspuid = shujus[x].split('_')[4].replace('"', '')
            from_pos = shujus[x].replace('"', '')
            # print(from_pos)
            item['pspuid'] = pspuid  # 商品的id
            item['from_pos'] = from_pos  # 商品的代号
            yield item
            yield Request(self.url.format(keyword=self.keyword, title=item['title'], id=item['pspuid'],
                                          from_pos=item['from_pos']), callback=self.parse_url)
    def parse_url(self,response):
        try:
            item = TaobaoItem()
            pat = re.compile(r'"spuId":"(\d{7})".*?"params":\[(.*?)\],"tag"', re.S)
            cen = re.findall(pat, response.text)
            pspuid = cen[0][0]
            parameter = cen[0][1].replace('"name":', '').replace('"value":', '').replace('"', '')
            item['pspuid'] = pspuid
            item['parameter'] = parameter#具体参数
            self.count+=1
            print(self.count)
            # print(item)
            yield item
        except IndexError:
            return ''

