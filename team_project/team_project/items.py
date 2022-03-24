import scrapy


class TeamProjectItem(scrapy.Item):
    author = scrapy.Field()


class NewsItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()


class RmrbItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()


class SouhuItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    reading = scrapy.Field()


class SinaItem(scrapy.Item):
    head = scrapy.Field()
    content = scrapy.Field()


class HongLouItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
