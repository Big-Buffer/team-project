import scrapy


class TeamProjectItem(scrapy.Item):
    author = scrapy.Field()


class RmrbItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()


class SouhuItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    reading = scrapy.Field()
