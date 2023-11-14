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

        for agency_link in response.css('a.Table-row::attr(href)').getall():
            agency_url = response.urljoin(agency_link)
            yield scrapy.Request(agency_url, callback=self.parse_agency)

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

    async def parse_agency(self, response):
        # Extracting the department's name
        full_department_name = response.css('h1.Article-p.Article-p--heading::text').get()
        # Splitting the name and keeping only the first part
        department_name = full_department_name.split(' - ')[0] if full_department_name else ''

        # Extracting details from the definition list
        details = {'Department Name': department_name}
        dt_elements = response.css('div.DefList dl dt::text').getall()
        dd_elements = response.css('div.DefList dl dd::text').getall()

        for dt, dd in zip(dt_elements, dd_elements):
            details[dt.strip(':')] = dd.strip()

        # Handling the website separately since it's an anchor tag
        website_url = response.css('div.DefList dl dd a::attr(href)').get()

        # Adding website to the details
        if website_url:
            details['Website'] = website_url

        # Your code to process the details
        # Example: yield details
        yield details

        # Remember to handle the Playwright page if needed
        if response.meta.get("playwright_page"):
            page = response.meta["playwright_page"]
            await page.close()

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
