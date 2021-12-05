from scrapy_redis.spiders import RedisSpider
from ..items import RmrbItem
import scrapy


class RmrbSpiderSpider(RedisSpider):
    name = 'rmrb_spider'
    # allowed_domains = ['paper.people.com.cn']
    # start_urls = ['http://paper.people.com.cn/']
    redis_key = "rmrb:"

    def parse(self, response):
        title_list = response.xpath('//div[@class="news"]/ul/li')
        for li in title_list:
            item = RmrbItem()
            title = li.xpath('./a/text()').get()
            item['title'] = title
            # print(title)

            # 解析详情页
            href = li.xpath('./a/@href').get()
            info_url = response.urljoin(href)
            yield scrapy.Request(
                url=info_url,
                callback=self.info_parse,
                meta={'item': item}
            )

        # 多页面处理
        next = response.xpath('//div[@class="swiper-container"]/div/a/@href').getall()
        for i in next:
            next_url = response.urljoin(i)
            yield scrapy.Request(next_url)

    def info_parse(self, response):
        item = response.meta['item']
        author = response.xpath('//div[@class="article"]/p/text()')[1].get().strip()
        if author == '':
            author = '人民日报编辑部'
        item['author'] = author
        # print(item)
        yield item

    custom_settings = {
        'ITEM_PIPELINES': {
            'team_project.pipelines.RmrbPipeline': 300},
    }
