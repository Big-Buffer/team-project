import scrapy


class TeamProjectItem(scrapy.Item):
    author = scrapy.Field()


class RmrbItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    pass


