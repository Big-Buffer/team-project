from scrapy_redis.spiders import RedisSpider
from ..items import TeamProjectItem


class TestSpider(RedisSpider):
    name = 'test'
    item = TeamProjectItem()
    # start_urls = [
    #     'https://www.qiushibaike.com/hot/page/1/'
    # ]
    redis_key = "test:start_urls"

    def parse(self, response):
        divs = response.xpath("//div[@class='col1 old-style-col1']/div")

        for div in divs:
            author = div.xpath(".//div/a/h2/text()").get().strip()

            item = TeamProjectItem(author=author)
            yield item

    custom_settings = {
        'team_project.pipelines.TeamProjectPipeline': 300,
    }
