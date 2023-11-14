# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re


class DepartmentNameFormattingPipeline:
    def process_item(self, item, spider):
        if item.get('department_name'):
            item['department_name'] = item['department_name'].split(' - ')[0]
        return item

class PhoneNumberFormattingPipeline:
    def process_item(self, item, spider):
        if item.get('phone_'):
            phone_ = re.sub(r'\D', '', item['phone_'])  # Remove non-digit characters
            formatted_phone = f"({phone_[:3]})-{phone_[3:6]}-{phone_[6:]}"
            item['phone_'] = formatted_phone
        return item

class FaxNumberFormattingPipeline:
    def process_item(self, item, spider):
        if item.get('fax_'):
            fax_ = re.sub(r'\D', '', item['fax_'])  # Remove non-digit characters
            formatted_fax = f"({fax_[:3]})-{fax_[3:6]}-{fax_[6:]}"
            item['fax_'] = formatted_fax
        return item
