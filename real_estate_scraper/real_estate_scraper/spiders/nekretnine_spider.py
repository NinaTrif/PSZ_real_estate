from ..items import *


class NekretnineSpider(scrapy.Spider):
    name = "real_estate"

    def start_requests(self):
        urls = [
            'https://www.nekretnine.rs/stambeni-objekti/stanovi/izdavanje-prodaja/prodaja/lista/po-stranici/10/',
            'https://www.nekretnine.rs/stambeni-objekti/stanovi/izdavanje-prodaja/izdavanje/lista/po-stranici/10/',
            'https://www.nekretnine.rs/stambeni-objekti/kuce/izdavanje-prodaja/prodaja/lista/po-stranici/10/',
            'https://www.nekretnine.rs/stambeni-objekti/kuce/izdavanje-prodaja/izdavanje/lista/po-stranici/10/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        offers = response.css('h2 a::attr(href)')
        for href in offers:
            yield response.follow(url=href.get(), callback=self.parse_offer)

        next_page = response.css("a.pagination-arrow.arrow-right::attr(href)").get()
        if next_page is not None:
            yield response.follow(url=next_page, callback=self.parse)

    def parse_offer(self, response):
        _offer_id = self.parse_offer_id(response)
        _estate_type = self.parse_estate_type(response)
        _offer_type = self.parse_offer_type(response)
        _city, _district, _street = self.parse_location(response)
        _size = self.parse_size(response)
        _year = self.parse_year(response)
        _land_area = self.parse_land_area(response)
        _total_floors = self.parse_total_floors(response)
        _floor = self.parse_floor(response)
        _registration = self.parse_registration(response)
        _heating = self.parse_heating(response)
        _rooms = self.parse_rooms(response)
        _bathrooms = self.parse_bathrooms(response)
        _parking = self.parse_parking(response)
        _elevator = self.parse_elevator(response)
        _balcony = self.parse_balcony(response)
        _state = self.parse_state(response)
        _price = self.parse_price(response)

        item = RealEstateScraperItem()
        item['offer_id'] = _offer_id
        item['estate_type'] = _estate_type
        item['offer_type'] = _offer_type
        item['city'] = _city
        item['district'] = _district
        item['street'] = _street
        item['size'] = _size
        item['year'] = _year
        item['land_area'] = _land_area
        item['total_floors'] = _total_floors
        item['floor'] = _floor
        item['registration'] = _registration
        item['heating'] = _heating
        item['rooms'] = _rooms
        item['bathrooms'] = _bathrooms
        item['parking'] = _parking
        item['elevator'] = _elevator
        item['balcony'] = _balcony
        item['state'] = _state
        item['price'] = _price
        # skip storing the item if there is no price (target variable)
        if _price is not None:
            yield item

    def parse_offer_id(self, response):
        return response.request.url

    def parse_estate_type(self, response):
        if 'stan' in response.css('h2.detail-seo-subtitle::text').extract()[0]:
            return 'stan'
        else:
            return 'kuca'

    def parse_offer_type(self, response):
        if 'Prodaja' in response.css('h2.detail-seo-subtitle::text').extract()[0]:
            return 'prodaja'
        else:
            return 'iznajmljivanje'

    def parse_location(self, response):
        location = response.css('div.property__location ul li::text').extract()
        if location[0] != 'Srbija':
            return None, None, None
        city = None
        if len(location) > 2:
            city = location[2]
        district = None
        if len(location) > 3:
            district = location[3]
        street = None
        if len(location) > 4:
            street = location[4]
        return city, district, street

    def parse_size(self, response):
        try:
            size = response.css('h4.stickyBox__size::text').extract()[0]
            size.replace(' ', '')
            return int(size[0:size.find('m')])
        except Exception as e:
            return None

    def parse_year(self, response):
        details = response.css('div.property__amenities ul li::text').extract()
        amenity_values = response.css('div.property__amenities ul li strong::text').extract()
        for elem in details:
            if 'Godina izgradnje:' in elem:
                try:
                    return int(amenity_values[details.index(elem) // 2])
                except Exception as e:
                    return None
        return None

    def parse_land_area(self, response):
        details = response.css('div.property__main-details ul li span::text').extract()
        for elem in details:
            if 'Površina zemljišta:' in elem:
                try:
                    return float(details[details.index('Površina zemljišta:') + 1].strip().split(' ')[0])
                except Exception as e:
                    return None
        return None

    def parse_total_floors(self, response):
        details = response.css('div.property__amenities ul li::text').extract()
        amenity_values = response.css('div.property__amenities ul li strong::text').extract()
        total_floors = None
        for elem in details:
            if 'Ukupan broj spratova:' in elem or 'Ukupan brој spratova:' in elem:
                try:
                    total_floors = int(amenity_values[details.index(elem) // 2])
                except Exception as e:
                    total_floors = None
        return total_floors

    def parse_floor(self, response):
        details = response.css('div.property__amenities ul li::text').extract()
        amenity_values = response.css('div.property__amenities ul li strong::text').extract()
        floor = None
        for elem in details:
            if 'Spratnost:' in elem:
                try:
                    floor = int(amenity_values[details.index(elem) // 2])
                except Exception as e:
                    tmp = amenity_values[details.index(elem) // 2].split('\n')[1].strip()
                    if tmp == 'Prizemlje' or tmp == 'Visoko prizemlje' or tmp == 'Suteren':
                        floor = 0
        return floor

    def parse_registration(self, response):
        details = response.css('div.property__main-details ul li span::text').extract()
        for elem in details:
            if 'Uknjiženo:' in elem:
                return details[details.index('Uknjiženo:') + 1]
        return None

    def parse_heating(self, response):
        details = response.css('div.property__main-details ul li span::text').extract()
        for elem in details:
            if 'Grejanje:' in elem:
                try:
                    return None if details[details.index('Grejanje:') + 1] == '-' else details[
                        details.index('Grejanje:') + 1]
                except Exception as e:
                    return None
        return None

    def parse_rooms(self, response):
        details = response.css('div.property__main-details ul li span::text').extract()
        for elem in details:
            if 'Sobe:' in elem:
                try:
                    return int(details[details.index('Sobe:') + 1])
                except Exception as e:
                    return None
        return None

    def parse_bathrooms(self, response):
        details = response.css('div.property__amenities ul li::text').extract()
        amenity_values = response.css('div.property__amenities ul li strong::text').extract()
        for elem in details:
            if 'Broj kupatila:' in elem:
                try:
                    return int(amenity_values[details.index(elem) // 2])
                except Exception as e:
                    return None
        return None

    def parse_parking(self, response):
        for elem in response.css('div.property__amenities ul li::text').extract():
            if 'parking' in elem or 'Parking' in elem or 'garaza' in elem or 'Garaza' in elem or 'garaža' in elem or 'Garaža' in elem:
                return 'da'
        return 'ne'

    def parse_elevator(self, response):
        for elem in response.css('div.property__amenities ul li::text').extract():
            if 'Lift' in elem:
                return 'da'
        return 'ne'

    def parse_balcony(self, response):
        for elem in response.css('div.property__amenities ul li::text').extract():
            if 'Terasa' in elem or 'Lođa' in elem or 'Lodja' in elem or 'Balkon' in elem:
                return 'da'
        return 'ne'

    def parse_state(self, response):
        details = response.css('div.property__amenities ul li::text').extract()
        amenity_values = response.css('div.property__amenities ul li strong::text').extract()
        for elem in details:
            if 'Stanje nekretnine:' in elem:
                try:
                    return amenity_values[details.index(elem) // 2].split('\n')[1].strip()
                except Exception as e:
                    return None
        return None

    def parse_price(self, response):
        full_price = response.css('h4.stickyBox__price::text').extract()[0]
        # return None if there is no set price, silently drop this offer later
        try:
            price = "".join(full_price.split())
            price.replace(' ', '')
            return int(price[0:price.find('EUR')])
        except Exception as e:
            return None
