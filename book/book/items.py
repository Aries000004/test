# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    cen = scrapy.Field()
    name = scrapy.Field()
    time = scrapy.Field()
    zuozhe = scrapy.Field()
