#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
from scrapy import Request

from meizitu.items import PicItem


class MeizituSpider(scrapy.Spider):
    name = "meizitu"
    allow_domains = ["www.mzitu.com/"]
    start_urls = "http://www.mzitu.com/"
    base_urls = "http://www.mzitu.com/page/{0}"

    def start_requests(self):
        yield Request(url=self.start_urls, callback=self.parse_total_pages)

    '''
    #总页数
    '''

    def parse_total_pages(self, response):
        hxs = scrapy.Selector(response=response)
        total_pages = hxs.xpath("//a[@class='page-numbers']/text()").extract()[-1]
        for i in range(int(total_pages)):
            page_url = self.base_urls.format(i + 1)
            yield Request(url=page_url, callback=self.parse_page)

    '''
    解析每一页
    '''

    def parse_page(self, response):
        hxs = scrapy.Selector(response=response)
        post_url_list = hxs.xpath(
            "//div[@class='postlist']/ul[@id='pins']/li/span/a/@href").extract()
        post_name_list = hxs.xpath(
            "//div[@class='postlist']/ul[@id='pins']/li/span/a/text()").extract()
        for name, url in zip(post_name_list, post_url_list):
            yield Request(url=url, callback=self.pase_post)

    '''
    #解析每一张专辑
    '''

    def pase_post(self, response):
        base_url = response.url
        hxs = scrapy.Selector(response=response)
        total_pics = hxs.xpath("//div[@class='pagenavi']/a/span/text()")[-2].extract()
        for i in range(int(total_pics)):
            if i==0:
                pic_url = base_url
            else:
                pic_url = base_url + "/{0}".format(str(i + 1))
            yield Request(url=pic_url, callback=self.pase_img,
                          meta={"img_name": str(i + 1)})

    '''
    #解析每一张图片
    '''

    def pase_img(self, response):
        hxs = scrapy.Selector(response=response)
        src_uri = hxs.xpath("//div[@class='main-image']/p/a/img/@src")[0].extract()
        post_name = hxs.xpath("//div[@class='main-image']/p/a/img/@alt")[0].extract()
        pic_name = response.meta["img_name"]
        yield PicItem(folder_name=post_name, pic_url=src_uri, pic_name=pic_name + ".jpg")
