# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LitresItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    rating = scrapy.Field()
    genres = scrapy.Field()
    tags = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    ISBN = scrapy.Field()

    pass
