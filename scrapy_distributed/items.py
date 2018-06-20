# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from scrapy.loader.processors import MapCompose, Join
import re


class Product(Item):
    title = Field(
        input_proceesor=MapCompose(str.strip),
        output_processor=Join()
    )
    shop = Field()
    price = Field()
    comment = Field(
        input_processor=MapCompose(lambda i: str(int(10000 * float(re.search('(\d+)(\.\d+)?', i).group()))) + '+'
                        if '万' in set(i) else re.search('(\d+)', i).group(1) + '+')
    )
    keyword = Field()
    page = Field()
    time = Field()
