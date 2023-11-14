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

    # async def parse_agency(self, response):
    #     item = AgencyItem()
    #     # Extracting the department's name
    #     full_department_name = response.css('h1.Article-p.Article-p--heading::text').get()
    #     item['department_name'] = full_department_name.split(' - ')[0] if full_department_name else ''
    #     item['country'] = response.css('dd.DefList-description::text')[0].get()
    #     item['address'] = response.css('dd.DefList-description::text')[1].get()
    #     item['city'] = response.css('dd.DefList-description::text')[2].get()
    #     item['state'] = response.css('dd.DefList-description::text')[3].get()
    #     item['zip_code'] = response.css('dd.DefList-description::text')[4].get()
    #     item['county'] = response.css('dd.DefList-description::text')[5].get()
    #     item['phone_number'] = response.css('dd.DefList-description::text')[6].get()
    #     item['website'] = response.css('a.u-textClip::attr(href)').get()
    #     item['type'] = response.css('dd.DefList-description::text')[9].get()
    #     item['population_served'] = response.css('dd.DefList-description::text')[10].get()
    #     item['number_of_officers'] = response.css('dd.DefList-description::text')[11].get()
    #     item['directory_url'] = response.url
    #
    #     yield item
    #
    #     # Remember to handle the Playwright page if needed
    #     if response.meta.get("playwright_page"):
    #         page = response.meta["playwright_page"]
    #         await page.close()

    async def parse_agency(self, response):
        item = AgencyItem()

        item['department_name'] = response.css('h1.Article-p.Article-p--heading::text').get()
        # Initialize all fields to None
        for field in item.fields:
            item[field] = None

        # Define a mapping of labels to item fields
        field_mapping = {
            'Address 1': 'address1',
            'Address 2': 'address2',
            'City': 'city',
            'State': 'state',
            'Zip Code': 'zip_code',
            'County': 'county',
            'Phone #': 'phone_number',
            'Fax #': 'fax_number',
            'Website': 'website',
            'Type': 'type',
            'Population Served': 'population_served',
            'Number of Officers': 'number_of_officers',
            # Add more mappings as needed
        }

        # Extract label-value pairs
        labels = response.css('dt.DefList-term::text').getall()
        values = response.css('dd.DefList-description::text').getall()

        for label, value in zip(labels, values):
            field_name = field_mapping.get(label.strip(':'))
            if field_name:
                item[field_name] = value.strip()

        item['directory_url'] = response.url

        yield item

        # Close Playwright page if needed
        if response.meta.get("playwright_page"):
            page = response.meta["playwright_page"]
            await page.close()

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
