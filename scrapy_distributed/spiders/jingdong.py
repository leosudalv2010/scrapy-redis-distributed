# -*- coding: utf-8 -*-
import scrapy
from scrapy_distributed.settings import KEYWORDS, MAXPAGE
from scrapy_distributed.items import Product
from urllib.parse import quote
from scrapy.loader import ItemLoader
import datetime


class JingdongSpider(scrapy.Spider):
    name = 'jingdong'
    allowed_domains = ['jd.com']

    def start_requests(self):
        for keyword in KEYWORDS:
            for page in range(1, MAXPAGE + 1):
                url = 'https://search.jd.com/Search?keyword={0}&enc=utf-8&page={1}'.format(quote(keyword), page*2 - 1)
                yield scrapy.Request(url, meta={'keyword': keyword, 'page': str(page)}, callback=self.parse)

    def parse(self, response):
        products = response.xpath('//div[@id="J_main"]/div[@class="m-list"]//div[@id="J_goodsList"]/ul/li')
        keyword = response.meta['keyword']
        page = response.meta['page']
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for product in products:
            loader = ItemLoader(item=Product())
            loader.add_value('title', product.xpath('.//div[starts-with(@class, "p-name")]/a/em/text()').extract())
            loader.add_value('shop', product.xpath('.//div[@class="p-shop"]/span/a/@title').extract_first())
            loader.add_value('price', product.xpath('.//div[@class="p-price"]/strong/i/text()').extract_first())
            loader.add_value('comment', product.xpath('.//div[@class="p-commit"]/strong/a/text()').extract_first())
            loader.add_value('keyword', keyword)
            loader.add_value('page', page)
            loader.add_value('time', time)
            yield loader.load_item()
        self.logger.info('Page {} is completed'.format(page))
