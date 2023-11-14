from typing import Iterable

import scrapy
from scrapy import Request
from scrapy_playwright.page import PageMethod
from police1.items import AgencyItem

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

        for agency_link in response.css('a.Table-row::attr(href)').getall():
            agency_url = response.urljoin(agency_link)
            yield scrapy.Request(agency_url, callback=self.parse_agency)

        next_page_link_selector = response.xpath('//*[@id="department-list"]/div/div[2]/div/a')
        next_page_link = next_page_link_selector.xpath('@href').get()

        if next_page_link is not None:
            next_page_url = response.urljoin(next_page_link)
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

    async def parse_agency(self, response):
        item = AgencyItem()

        # Extracting the department's name
        item['department_name'] = response.css('h1.Article-p.Article-p--heading::text').get()

        # Extracting details from the definition list
        def_list = response.css('.DefList')
        for dl in def_list:
            dt_elements = dl.css('dt::text').getall()
            dd_elements = dl.css('dd::text, dd a::attr(href)').getall()

            for dt, dd in zip(dt_elements, dd_elements):
                key = dt.replace('#', '').strip(':').lower().replace(' ', '_')
                value = dd.strip()
                item[key] = value

        # Extracting website URL
        website_url_selector = response.css('dl.DefList dd a::attr(href)')
        website_url = website_url_selector.get()

        if website_url:
            item['website'] = website_url.strip()

        # Extracting the directory url
        item['directory_url'] = response.url

        yield item

        # Close the playwright page if needed
        if response.meta.get("playwright_page"):
            page = response.meta["playwright_page"]
            await page.close()

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
