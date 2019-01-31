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
    traffic = scrapy.Field()
    fd = scrapy.Field()
    pkh = scrapy.Field()
    uptime = scrapy.Field()
    speed_test = scrapy.Field()
    serp_desktop = scrapy.Field()
    serp_mobile = scrapy.Field()
    links = scrapy.Field()
    content = scrapy.Field()
    robots = scrapy.Field()
    y_alert = scrapy.Field()
    g_alert = scrapy.Field()
    exp_date = scrapy.Field()
    pages = scrapy.Field()
    y_index = scrapy.Field()
    g_index = scrapy.Field()
    # pass
