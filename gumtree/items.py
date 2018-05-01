# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GumtreeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    area = scrapy.Field()
    added_at = scrapy.Field()
    sold_by = scrapy.Field()
    rooms = scrapy.Field()
    url = scrapy.Field()
    description = scrapy.Field()
    inactive = scrapy.Field()
    updated_at = scrapy.Field()
