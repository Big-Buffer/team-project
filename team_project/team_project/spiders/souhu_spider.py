import scrapy
from ..items import SouhuItem
from scrapy_redis.spiders import RedisSpider


class souhu_spider(RedisSpider):
    name = 'souhu_spider'
    # url = 'https://news.sohu.com/'
    redis_key = "souhu:"
    # start_urls = ['https://news.sohu.com/']

    def parse(self, response, **kwargs):
        selector = scrapy.Selector(response)
        titles = selector.xpath('//div[@class="list16"]/ul/li/a/@title').getall()
        # for title in titles:
        #     print(title.get().strip())
        hrefs = selector.xpath('//div[@class="list16"]/ul/li/a/@href').getall()
        for href in hrefs:
            # print(href.get())
            yield scrapy.Request(url=response.urljoin(href), callback=self.parse_detail)

    def parse_detail(self, response):
        item = SouhuItem()
        selector = scrapy.Selector(response)
        title = selector.xpath('//h1/text()').getall()
        data = ''
        for t in title:
            data = t + data
        title = data.replace(' ', '').replace('\n', '')
        content = selector.xpath('//article/p/text()').getall()
        data = ''
        for con in content:
            data = con + data
        content = data.replace(' ', '').replace('\n', '')
        reading = selector.xpath('//span[@class="read-num"]/em/text()').getall()

        item['title'] = title
        item['content'] = content
        item['reading'] = reading
        # title = response.xpath('//h1/text()').get().strip()
        # content = response.xpath('//article/p').get()
        # reading = response.xpath('//span[@class="read-num"]').get()
        # print(title)
        yield item

    custom_settings = {
        'ITEM_PIPELINES': {
            'team_project.pipelines.SouhuPipeline': 300},
        'DOWNLOADER_MIDDLEWARES': {
            'team_project.middlewares.SouhuSeleniumMiddleware': 643,
        }
    }
