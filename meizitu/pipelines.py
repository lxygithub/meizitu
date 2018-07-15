# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import re

import requests
from scrapy.pipelines.images import ImagesPipeline

from meizitu.settings import IMAGES_STORE


class MzituScrapyPipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None):
        """
        :param request: 每一个图片下载管道请求
        :param response:
        :param info:
        :param strip :清洗Windows系统的文件夹非法字符，避免无法创建目录
        :return: 每套图的分类目录
        """
        item = request.meta['item']
        folder = item['folder_name']
        folder_strip = strip(folder)
        filename = IMAGES_STORE + "{0}\{1}".format(folder_strip, item["pic_name"])
        return filename

    def get_media_requests(self, item, info):
        default_headers = {
            'Host': 'i.meizitu.net',
            'Pragma': 'no-cache',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': "http://www.mzitu.com",
        }
        resp = requests.get(url=item["pic_url"], headers=default_headers)
        folder = item['folder_name']
        folder_strip = IMAGES_STORE+strip(folder)
        filename = "{0}/{1}".format(folder_strip, item["pic_name"])
        if not os.path.exists(folder_strip):
            os.makedirs(folder_strip)
            os.chdir(folder_strip)

        exist = os.path.exists(os.path.abspath(filename))
        if not exist:
            with open(filename,"ab") as f:
                f.write(resp.content)




def strip(path):
    """
    :param path: 需要清洗的文件夹名字
    :return: 清洗掉Windows系统非法文件夹名字的字符串
    """
    path = re.sub(r'[？\\*|“<>:/]', '', str(path))
    return path
