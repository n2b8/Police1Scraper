# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
from scrapy.exceptions import DropItem


class DepartmentNameFormattingPipeline:
    def process_item(self, item, spider):
        if item.get('department_name'):
            item['department_name'] = item['department_name'].split(' - ')[0]
        return item

class PhoneNumberFormattingPipeline(object):
    def process_item(self, item, spider):
        if 'phone_' in item:
            phone = item['phone_']
            formatted_phone = self.format_phone_number(phone)
            item['phone_'] = formatted_phone if formatted_phone else None
        return item

    def format_phone_number(self, phone):
        # Remove non-digit characters
        digits = re.sub(r'\D', '', phone)
        if len(digits) == 10:
            # Format the number as (123)-456-7890
            return f"({digits[:3]})-{digits[3:6]}-{digits[6:]}"
        else:
            return None

class FaxNumberFormattingPipeline(object):
    def process_item(self, item, spider):
        if 'fax_' in item:
            fax = item['fax_']
            formatted_fax = self.format_fax_number(fax)
            item['fax_'] = formatted_fax if formatted_fax else None
        return item

    def format_fax_number(self, fax):
        # Remove non-digit characters
        digits = re.sub(r'\D', '', fax)
        if len(digits) == 10:
            # Format the number as (123)-456-7890
            return f"({digits[:3]})-{digits[3:6]}-{digits[6:]}"
        else:
            return None

class ConvertOfficersToIntegerPipeline(object):
    def process_item(self, item, spider):
        if 'number_of_officers' in item:
            try:
                item['number_of_officers'] = int(item['number_of_officers'])
            except ValueError:
                item['number_of_officers'] = None  # Leave blank if not a valid number
        return item

class ProcessPopulationServedPipeline(object):
    def process_item(self, item, spider):
        if 'population_served' in item:
            population = item['population_served']
            formatted_population = self.format_population(population)
            item['population_served'] = formatted_population if formatted_population is not None else None
        return item

    def format_population(self, population):
        # Remove commas, spaces, and other non-numeric characters, except for M, K
        population = re.sub(r'[^\dMK]', '', population)

        if 'M' in population:
            # Convert from M (millions) to an integer
            number = re.sub(r'M', '', population)
            return int(number) * 1000000
        elif 'K' in population:
            # Convert from K (thousands) to an integer
            number = re.sub(r'K', '', population)
            return int(number) * 1000
        elif re.match(r'^\d+$', population):
            # Pure number without M or K
            return int(population)
        else:
            # Return None if the pattern does not match
            return None
