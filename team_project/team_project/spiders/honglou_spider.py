import requests
import scrapy
from ..items import HongLouItem
from scrapy_redis.spiders import RedisSpider
from scrapy import Spider

rootUrl = 'https://www.gdwxcn.com'


class HongLouSpider(Spider):
    name = 'hongLou'
    start_urls = ['https://www.gdwxcn.com/gdxs/hlm/']
    redis_key = 'hong:'

    def parse(self, response, **kwargs):
        hrefs = response.xpath('//div[@class="zhangjie"]/ul/li/a/@href').extract()
        for href in hrefs:
            yield scrapy.Request(url=rootUrl + href, callback=self.detail_parse)

    def detail_parse(self, response):
        item = HongLouItem()
        content = ""
        title = response.xpath('//div[@class="xsnr"]/h1/text()').extract()
        content_list = response.xpath('//div[@class="xstext"]').extract()
        # 将p标签里的文本内容合并到一起
        for content_one in content_list:
            content += content_one
        item['title'] = title
        item['content'] = content
        print(item)
        yield item

    custom_settings = {
        'ITEM_PIPELINES': {
            'team_project.pipelines.HongLouPipeline': 300},
    }
