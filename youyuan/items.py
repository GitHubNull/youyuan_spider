# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YouyuanItem(scrapy.Item):
    nick_name = scrapy.Field()
    age = scrapy.Field()
    address = scrapy.Field()
    education = scrapy.Field()
    in_come = scrapy.Field()
    header_img_url = scrapy.Field()
    main_page_url = scrapy.Field()
    spider_datetime = scrapy.Field()
    spider_com = scrapy.Field()

