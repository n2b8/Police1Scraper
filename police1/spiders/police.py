from typing import Iterable

import scrapy
from scrapy import Request
from scrapy_playwright.page import PageMethod


class PoliceSpider(scrapy.Spider):
    name = "police"
    allowed_domains = ["www.police1.com"]
    start_urls = ["https://www.police1.com/law-enforcement-directory/search"]

    def start_requests(self):
        url = "https://www.police1.com/law-enforcement-directory/search"
        yield scrapy.Request(url, meta=dict(
            playwright=True,
            playwright_include_page=True,
            playwright_page_methods=[
                PageMethod("wait_for_selector", "a.Table-row"), # 25 per page
            ],
            errback=self.errback,
        ))

    async def parse(self, response):
        page = response.meta["playwright_page"]
        await page.close()

        for link in response.css('a.Table-row::attr(href)'):
            print(link)


        next_page_link_selector = response.xpath('//*[@id="department-list"]/div/div[2]/div/a')
        next_page_link = next_page_link_selector.xpath('@href').get()


        if next_page_link is not None:
            next_page_url = self.start_urls[0] + next_page_link
            print(f"Next button was pressed!, next url is {next_page_url}")
            yield scrapy.Request(next_page_url, meta=dict(
                playwright = True,
                playwright_include_page = True,
                playwright_page_methods = [
                    PageMethod('wait_for_selector', 'a.Table-row'),
                ],
                errback=self.errback,
            ))
        else:
            print("Next button was not pressed")

    async def parse_table(self, response):
        yield print("SUCCESS!!")


    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
