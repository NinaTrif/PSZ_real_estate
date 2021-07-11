import mysql.connector


class DatabaseManager(object):
    instance = None
    cursor = None

    def __init__(self):
        self.connect()

    def connect(self):
        self.instance = mysql.connector.connect(
            host="localhost",
            user="psz",
            password="psz2021",
            database='real_estate_db'
        )

        self.cursor = self.instance.cursor(prepared=True)

        self.cursor.execute("""create table if not exists real_estate(
                                            offer_id text not null,
                                            estate_type text not null,
                                            offer_type text not null,
                                            city text,
                                            district text,
                                            street text,
                                            size integer,
                                            year integer,
                                            land_area float,
                                            total_floors integer,
                                            floor integer,
                                            registration text,
                                            heating text,
                                            rooms integer,
                                            bathrooms integer,
                                            parking text,
                                            elevator text,
                                            balcony text,
                                            state text,
                                            price integer not null
                                        )""")

    def store_item(self, item):
        # use parameterized query, as it provides None value handling (None -> NULL)
        insert_query = """insert into real_estate values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        insert_tuple = (item['offer_id'], item['estate_type'], item['offer_type'], item['city'],
                        item['district'], item['street'], item['size'], item['year'],
                        item['land_area'], item['total_floors'], item['floor'], item['registration'],
                        item['heating'], item['rooms'], item['bathrooms'], item['parking'],
                        item['elevator'], item['balcony'], item['state'], item['price'])
        self.cursor.execute(insert_query, insert_tuple)
        self.instance.commit()
