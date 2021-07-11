# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RealEstateScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    offer_id = scrapy.Field()
    estate_type = scrapy.Field()
    offer_type = scrapy.Field()
    city = scrapy.Field()
    district = scrapy.Field()
    street = scrapy.Field()
    size = scrapy.Field()
    year = scrapy.Field()
    land_area = scrapy.Field()
    total_floors = scrapy.Field()
    floor = scrapy.Field()
    registration = scrapy.Field()
    heating = scrapy.Field()
    rooms = scrapy.Field()
    bathrooms = scrapy.Field()
    parking = scrapy.Field()
    elevator = scrapy.Field()
    balcony = scrapy.Field()
    state = scrapy.Field()
    price = scrapy.Field()
