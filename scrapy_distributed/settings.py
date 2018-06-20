# -*- coding: utf-8 -*-

# Scrapy settings for scrapy_distributed project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'scrapy_distributed'

SPIDER_MODULES = ['scrapy_distributed.spiders']
NEWSPIDER_MODULE = 'scrapy_distributed.spiders'

KEYWORDS = ['shirt']
MAXPAGE = 100

DOWNLOADER_MIDDLEWARES = {
    'scrapy_distributed.middlewares.SeleniumMiddleware': 300
}

ITEM_PIPELINES = {
    'scrapy_distributed.pipelines.MySQLPipeline': 300
}
FEED_EXPORT_ENCODING = 'utf8'

# Scrapy-Redis related settings
SCHEDULER = 'scrapy_redis.scheduler.Scheduler'
DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'
REDIS_URL = 'redis://:sd89fjmn12s5dsf5x@192.168.2.200:6379'

LOG_FILE = 'log'
LOG_LEVEL = 'INFO'


# Obey robots.txt rules
ROBOTSTXT_OBEY = False

