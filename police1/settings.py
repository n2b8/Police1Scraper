# Scrapy settings for police1 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import os
from dotenv import load_dotenv

load_dotenv()

BOT_NAME = "police1"

SPIDER_MODULES = ["police1.spiders"]
NEWSPIDER_MODULE = "police1.spiders"

# Database settings
COCKROACHDB_PW = os.environ['COCKROACHDB_PW']
COCKROACHDB_DB = os.environ['COCKROACHDB_DB']
COCKROACHDB_PORT = os.environ['COCKROACHDB_PORT']
COCKROACHDB_CLUSTER = os.environ['COCKROACHDB_CLUSTER']
COCKROACHDB_USER = os.environ['COCKROACHDB_USER']
DB_URI = "postgresql://" + COCKROACHDB_USER + ":" + COCKROACHDB_PW + "@" + COCKROACHDB_CLUSTER + ".cockroachlabs.cloud:" + COCKROACHDB_PORT + "/" + COCKROACHDB_DB + "?sslmode=verify-full"

JOBDIR = 'crawls/spider-1'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "police1 (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "police1.middlewares.Police1SpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
SCRAPEOPS_API_KEY = os.environ['SCRAPEOPS_API_KEY']
SCRAPEOPS_FAKE_HEADERS_ENABLED = False
SCRAPEOPS_FAKE_USER_AGENT_ENABLED = True
SCRAPEOPS_FAKE_HEADERS_ENDPOINT = 'https://headers.scrapeops.io/v1/browser-headers'
SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT = 'https://headers.scrapeops.io/v1/user-agents'
SCRAPEOPS_NUM_RESULTS = 25

# Adding ScrapeOps monitoring
EXTENSIONS = {
    'scrapeops_scrapy.extension.ScrapeOpsMonitor': 500,
}
DOWNLOADER_MIDDLEWARES = {
    # 'police1.middlewares.ScrapeOpsFakeBrowserHeadersMiddleware': 400,
    'police1.middlewares.ScrapeOpsFakeUserAgentMiddleware': 401,
    'scrapeops_scrapy.middleware.retry.RetryMiddleware': 550,
    'scrapeopes.downloadermiddlewares.retry.RetryMiddleware': None,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "police1.pipelines.DepartmentNameFormattingPipeline": 300,
    "police1.pipelines.PhoneNumberFormattingPipeline": 301,
    "police1.pipelines.FaxNumberFormattingPipeline": 302,
    "police1.pipelines.ConvertOfficersToIntegerPipeline": 303,
    "police1.pipelines.ProcessPopulationServedPipeline": 304,
    "police1.pipelines.PostgresPipeline": 305,
}

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
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

LOG_FILE = 'scrapy_output.log'
LOG_LEVEL = 'DEBUG'  # Choose your logging level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL)

