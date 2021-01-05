# -*- coding: utf-8 -*-

# Scrapy settings for JdSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import datetime
import os
toDay = datetime.datetime.now()





BOT_NAME = 'JdSpider'

SPIDER_MODULES = ['JdSpider.spiders']
NEWSPIDER_MODULE = 'JdSpider.spiders'


# f_path = os.getcwd() + '\\log'
# if not os.path.exists(f_path):
#     os.makedirs(f_path)
# logFilePath = f_path + '\\log_{}_{}_{}.log'.format(toDay.year,toDay.month,toDay.day)
# LOG_FILE = logFilePath
# #LOG_LEVEL = 'INFO'
# #LOG_LEVEL = 'DEBUG'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'JdSpider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
    #'JdSpider.middlewares.JdspiderSpiderMiddleware': 543,

# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   #'JdSpider.middlewares.JdspiderDownloaderMiddleware': 543,
   'JdSpider.middlewares.UserAgentDownloadMiddleware':543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    #'JdSpider.pipelines.JdspiderPipeline': 300,
# #'JdSpider.pipelines.MysqlTwistedPipline':333,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
MYSQL_HOST = '127.0.0.1'
MYSQL_DBNAME = 'jing_dong'
MYSQL_USER = 'root'
MYSQL_PASSWORD = '123456'
MYSQL_PORT = 3306




#SCRAPY-REDIS配置
#确保reques存到redis   scheduler.py
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
#确保爬虫共享相同的去重指纹
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
#设置redis为item pipeline
ITEM_PIPELINES = {
    #'ZhihuHotQusSpider.pipelines.ZhihuhotqusspiderPipeline': 200,
    'scrapy_redis.pipelines.RedisPipeline':300
}
#在redis中保持scrapy-redis用到的队列，不会清理redis中的队列，从而实现暂停，恢复爬虫的功能
SCHEDULER_PERSIST = True
#
REDIS_HOST = '192.168.1.102'
REDIS_PORT = 6379
