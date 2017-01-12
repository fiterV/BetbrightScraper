# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyparserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    raceName = scrapy.Field()
    raceId = scrapy.Field()
    participantName = scrapy.Field()
    participantId = scrapy.Field()
    clothNumber = scrapy.Field()
    time = scrapy.Field()
    odds = scrapy.Field()

