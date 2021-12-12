import scrapy
from ..items import SinaItem
from scrapy_redis.spiders import RedisSpider


class ChinanewsSpider(RedisSpider):
    name = 'sina'
    # allowed_domains = ['news.sina.com.cn']
    # start_urls = ['https://news.sina.com.cn/china/']
    redis_key = 'sina:'

    def parse(self, response):
        hrefs = response.xpath('//div[@style="display:none;"]/ul/li/a/@href').extract()
        for href in hrefs:
            yield scrapy.Request(url=href, callback=self.detail_parse)

    def detail_parse(self, response):
        item = SinaItem()
        content = ""
        head = response.xpath('//h1[@class="main-title"]/text()').extract()
        content_list = response.xpath('//div[@id="article"]/p/text()').extract()
        # 将p标签里的文本内容合并到一起
        for content_one in content_list:
            content += content_one
        item['head'] = head
        item['content'] = content
        yield item

    custom_settings = {
        'ITEM_PIPELINES': {
            'team_project.pipelines.SinaPipeline': 300},
    }
