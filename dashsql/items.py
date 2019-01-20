# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DashsqlItem(scrapy.Item):
    domain_id = scrapy.Field()
    subdomain_id = scrapy.Field()
    title = scrapy.Field()
    status = scrapy.Field()
    response_len = scrapy.Field()
    pass
