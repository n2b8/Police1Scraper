# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AgencyItem(scrapy.Item):
    department_name = scrapy.Field()
    country = scrapy.Field()
    address_1 = scrapy.Field()
    address_2 = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    zip_code = scrapy.Field()
    county = scrapy.Field()
    phone_ = scrapy.Field()
    fax_ = scrapy.Field()
    website = scrapy.Field()
    type = scrapy.Field()
    population_served = scrapy.Field()
    number_of_officers = scrapy.Field()
    directory_url = scrapy.Field()
