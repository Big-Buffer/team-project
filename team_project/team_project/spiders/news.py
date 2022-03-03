import logging
from urllib.parse import urlparse

from scrapy_redis.spiders import RedisSpider
from ..items import NewsItem
import scrapy
from ..log import Log


class NewsSpider(RedisSpider):
    name = 'news'
    # start_urls = ['http://paper.people.com.cn/']
    # start_urls = ['https://news.sohu.com/']
    # start_urls = ['https://news.sina.com.cn/china/']
    redis_key = "news:"
    custom_settings = {
        'ITEM_PIPELINES': {
            'team_project.pipelines.NewsPipeline': 500},
    }
    logger = logging.getLogger('stat')
    def __init__(self):
        self.s = Log()

    def parse(self, response, **kwargs):
        self.s.start_time()
        if urlparse(response.url).netloc == "paper.people.com.cn":
            pass
            title_list = response.xpath('//div[@class="news"]/ul/li')
            for li in title_list:
                item = NewsItem()
                title = li.xpath('./a/text()').get()
                item['title'] = title
                # print(title)

                # 解析详情页
                href = li.xpath('./a/@href').get()
                info_url = response.urljoin(href)
                yield scrapy.Request(
                    url=info_url,
                    callback=self.rmrb_parse,
                    meta={'item': item}
                )

            # 多页面处理
            next_page = response.xpath('//div[@class="swiper-container"]/div/a/@href').getall()
            for i in next_page:
                next_url = response.urljoin(i)
                yield scrapy.Request(next_url)
        elif urlparse(response.url).netloc == "news.sina.com.cn":
            hrefs = response.xpath('//div[@style="display:none;"]/ul/li/a/@href').extract()
            for href in hrefs:
                yield scrapy.Request(url=href, callback=self.sina_parse)

        elif urlparse(response.url).netloc == "news.sohu.com" or urlparse(response.url).netloc == "sohu.com":
            selector = scrapy.Selector(response)
            hrefs = selector.xpath('//div[@class="list16"]/ul/li/a/@href').getall()
            for href in hrefs:
                # print(href.get())
                yield scrapy.Request(url=response.urljoin(href), callback=self.souhu_parse)
        self.s.end_time()

    def rmrb_parse(self, response):
        item = response.meta['item']
        content = response.xpath('//div[@id="ozoom"]/p/text()')[1].get().strip()
        data = ""
        for con in content:
            data += con
        item['content'] = data.replace(' ', '').replace('\n', '')
        # print(item)
        if item['title'] == '' or item['content'] == '':
            pass
        else:
            yield item

    def sina_parse(self, response):
        item = NewsItem()
        title = ""
        content = ""
        title_list = response.xpath('//h1[@class="main-title"]/text()').extract()
        content_list = response.xpath('//div[@id="article"]/p/text()').extract()
        for title_one in title_list:
            title += title_one
        for content_one in content_list:
            content += content_one
        if title == '' or content == '':
            pass
        else:
            item['title'] = title
            item['content'] = content.replace(' ', '').replace('\n', '')
            yield item

    def souhu_parse(self, response):
        item = NewsItem()
        selector = scrapy.Selector(response)
        title = selector.xpath('//h1/text()').getall()
        data = ''
        for t in title:
            data += t
        title = data.replace(' ', '').replace('\n', '')
        content = selector.xpath('//article/p/text()').getall()
        data = ''
        for con in content:
            data += con
        content = data.replace(' ', '').replace('\n', '')
        if title == '' or content == '':
            pass
        else:
            item['title'] = title
            item['content'] = content
            yield item
