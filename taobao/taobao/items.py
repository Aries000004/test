# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TaobaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pspuid =scrapy.Field()
    from_pos =scrapy.Field()
    price =scrapy.Field()
    title =scrapy.Field()
    month_sales =scrapy.Field()
    charcteristic =scrapy.Field()
    parameter = scrapy.Field()
