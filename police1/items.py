# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AgencyItem(scrapy.Item):
    department_name = scrapy.Field()
    country = scrapy.Field()
    address1 = scrapy.Field()
    address2 = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    zip_code = scrapy.Field()
    county = scrapy.Field()
    phone_number = scrapy.Field()
    fax_number = scrapy.Field()
    website = scrapy.Field()
    type = scrapy.Field()
    population_served = scrapy.Field()
    number_of_officers = scrapy.Field()
    directory_url = scrapy.Field()
