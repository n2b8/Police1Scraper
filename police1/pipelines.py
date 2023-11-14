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
            if formatted_phone:
                item['phone_'] = formatted_phone
            else:
                raise DropItem(f"Invalid phone number format: {phone}")
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
            if formatted_fax:
                item['fax_'] = formatted_fax
            else:
                raise DropItem(f"Invalid fax number format: {fax}")
        return item

    def format_fax_number(self, fax):
        # Remove non-digit characters
        digits = re.sub(r'\D', '', fax)
        if len(digits) == 10:
            # Format the number as (123)-456-7890
            return f"({digits[:3]})-{digits[3:6]}-{digits[6:]}"
        else:
            return None
