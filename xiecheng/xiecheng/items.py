# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XiechengItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Destination = scrapy.Field()
    Destination_num = scrapy.Field()
    Destination_url = scrapy.Field()

