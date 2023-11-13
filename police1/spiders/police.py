from typing import Iterable

import scrapy
from scrapy import Request
from scrapy_playwright.page import PageMethod


class PoliceSpider(scrapy.Spider):
    name = "police"
    allowed_domains = ["www.police1.com"]

    # start_urls = ["https://www.police1.com/law-enforcement-directory/search/"]

    def start_requests(self):
        url = "https://www.police1.com/law-enforcement-directory/search/"
        yield scrapy.Request(url, meta=dict(
            playwright=True,
            playwright_include_page=True,
            playwright_page_methods=[
                PageMethod("wait_for_selector", "a.Table-row"),
                PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),
                PageMethod("wait_for_selector", "a.Table-row:nth-child(26)"),  # 25 per page
            ],
            errback=self.errback,
        ))

    async def parse(self, response):
        page = response.meta["playwright_page"]
        await page.close()
        links = response.css('a.Table-row::attr(href)').getall()
        number = 0
        for link in links:
            number += 1
            yield print(f'Link #{number}: ', link)


    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
