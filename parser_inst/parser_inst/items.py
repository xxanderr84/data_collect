# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ParserInstItem(scrapy.Item):
    # define the fields for your item here like:
    user_id = scrapy.Field()
    photo = scrapy.Field()
    follow_name = scrapy.Field()
    follow_id = scrapy.Field()
    follow_full_name = scrapy.Field()
    collection = scrapy.Field()
    _id = scrapy.Field()
    pass
