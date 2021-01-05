# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JdspiderItem(scrapy.Item):
    # define the fields for your item here like:
    website = scrapy.Field()
    brand = scrapy.Field()
    shop_name = scrapy.Field()
    shop_url = scrapy.Field()
    good_sku = scrapy.Field()
    good_title = scrapy.Field()
    good_price = scrapy.Field()
    good_detail = scrapy.Field()
    good_color = scrapy.Field()
    good_tips = scrapy.Field()


class JdSpider2Item(scrapy.Item):

    sku = scrapy.Field()
    brand = scrapy.Field()
    price = scrapy.Field()
    title = scrapy.Field()
    shop_name = scrapy.Field()
    good_name = scrapy.Field()
    cpu = scrapy.Field()
    memory = scrapy.Field()
    ssd = scrapy.Field()
    gpu_model = scrapy.Field()
    gpu_type = scrapy.Field()
    weight = scrapy.Field()
    color = scrapy.Field()
    computer_type = scrapy.Field()
    thickness = scrapy.Field()
    series = scrapy.Field()
    pixel = scrapy.Field()
    screen_hz = scrapy.Field()
    sku_url = scrapy.Field()

class JdSpiderCommentItem(scrapy.Item):
    sku = scrapy.Field()
    comment = scrapy.Field()
    good_comment_rate = scrapy.Field()
    bad_comment_rate = scrapy.Field()
