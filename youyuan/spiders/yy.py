# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.spiders import Rule
from youyuan.items import YouyuanItem
from datetime import datetime


class YySpider(RedisCrawlSpider):
    name = 'yy'
    # allowed_domains = ['youyuan.com']
    # start_urls = ['http://youyuan.com/']
    redis_key = 'YySpider:start_urls'

    re_page_url = LinkExtractor(allow=(r'http://www.youyuan.com/find/beijing/mm18-25/advance-0-0-0-0-0-0-0/p1\d+/'))
    rules = (
        # Rule(LinkExtractor(allow=(r'http://www.youyuan.com/find/.*'))),
        Rule(re_page_url, callback='parse_item', follow=True),
    )

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(YySpider, self).__init__(*args, **kwargs)


    def parse_item(self, response):
        user_item_list = response.xpath('//li[contains(@class,"search_user_item")]')
        self.log('user item len: {}'.format(len(user_item_list)))
        if 0 >= len(user_item_list):
            yield None

        for user_item in user_item_list:
            nick_name = user_item.xpath('./dl/dd/a/strong/text()').extract_first()

            tail_info = user_item.xpath('./dl/dd/font/text()')

            age = 'NULL'
            address = 'NULL'
            education = 'NULL'
            in_come = 'NULL'

            if 1 <= len(tail_info):
                tail_info = tail_info.extract()
                if 1 <= len(tail_info):
                    age = tail_info[0].strip(' ').split('|')[0].strip()
                    address = tail_info[0].strip(' ').split('|')[1].strip()
                    education = tail_info[1].strip(' ').split('|')[0].strip()
                    in_come = tail_info[1].strip(' ').split('|')[1].strip()

            header_img_url = user_item.xpath('./dl/dt/a/img/@src')
            if 0 < len(header_img_url):
                header_img_url = header_img_url.extract_first()
            else:
                header_img_url = 'NULL'

            main_page_url = user_item.xpath('./dl/dt/a/@href')
            if 0 < len(main_page_url):
                main_page_url = 'http://www.youyuan.com/' + main_page_url.extract_first()
            else:
                main_page_url = 'NULL'

            item = YouyuanItem()

            item['nick_name'] = nick_name
            item['age'] = age
            item['address'] = address
            item['education'] = education
            item['in_come'] = in_come
            item['header_img_url'] = header_img_url
            item['main_page_url'] = main_page_url
            item['spider_datetime'] = datetime.timestamp(datetime.now())
            item['spider_com'] = 'youyuan.com'

            yield item

    def get_next_page(self, value):
        self.log('*'*80)
        if 0 < len(value):
            next_page_url = 'http://www.youyuan.com' + value.extract_first()
            if 0 < len(next_page_url):
                return next_page_url
        else:
            return None

