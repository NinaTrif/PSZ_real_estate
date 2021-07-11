# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .db_manager import DatabaseManager


class RealEstateScraperPipeline:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def process_item(self, item, spider):
        self.db_manager.store_item(item)
        return item
