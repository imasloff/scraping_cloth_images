# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ClothItem(scrapy.Item):
    id = scrapy.Field()
    category = scrapy.Field()
    unisex = scrapy.Field()
    title = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
