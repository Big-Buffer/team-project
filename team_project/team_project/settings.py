BOT_NAME = 'team_project'

SPIDER_MODULES = ['team_project.spiders']
NEWSPIDER_MODULE = 'team_project.spiders'

# 更改 USER_AGENT配置
USER_AGENT = 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'

DOWNLOADER_MIDDLEWARES = {
    'team_project.middlewares.RandomProxyMiddleware': 543,
    # TODO:暂时去掉
    # 'team_project.middlewares.SeleniumMiddleware': 643,
}

ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {
                  'scrapy_redis.pipelines.RedisPipeline': 400
                  }

# 使用scrapy-redis组件去重队列
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# 使用scrapy-redis自己的调度器
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# 是否允许暂停
SCHEDULER_PERSIST = True

REDIS_HOST = "139.196.110.245"
REDIS_PORT = 6379
