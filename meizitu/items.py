# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PicItem(scrapy.Item):
    folder_name = scrapy.Field()
    pic_url = scrapy.Field()
    pic_name = scrapy.Field()
    filename = scrapy.Field()
