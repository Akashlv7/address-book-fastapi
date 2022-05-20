import sqlite3
import itertools

from geopy.distance import geodesic

"""
1. sqlite - Used for Database operations
2. itertools - Used for data manipulation
3. geopy - Used to find the co-ordinates with in given range.

"""


class Address:

    db_connect = sqlite3.connect("address_book.db")
    db_cursor = db_connect.cursor()
    db_cursor.execute("""
                        CREATE TABLE IF NOT EXISTS addresses (
                            name TEXT  PRIMARY KEY   NOT NULL,
                            latitude       REAL     NOT NULL,
                            longitude      REAL     NOT NULL
                        )
                    """)

    def __init__(self, address_name=None, latitude=None, longitude=None):
        self.latitude = latitude
        self.longitude = longitude
        self.address_name = address_name


    @classmethod
    def create_database(cls):
        """Method that creates the addresses table if the table does not exist
        """
        cls.db_cursor.execute("""
                        CREATE TABLE IF NOT EXISTS addresses (
                            name TEXT  PRIMARY KEY   NOT NULL,
                            latitude       REAL     NOT NULL,
                            longitude      REAL     NOT NULL
                        )
                """)


    @classmethod
    def db_commit(cls):
        """Method to commit the changes done on the database
        """
        cls.db_connect.commit()


    @classmethod
    def db_close(cls):
        """Method to close the database connection
        """
        cls.db_connect.close()


    @classmethod
    def get_address(cls, query_address_name=None):
        """Method to get the address by name and to get all addresses present in the book from DB
        """
        if query_address_name == None:
            query = """SELECT * FROM addresses"""

        else:
            query = f"""
                        SELECT * FROM addresses
                        WHERE name = '{query_address_name}'
                    """
        cls.db_cursor.execute(query)
        rows = cls.db_cursor.fetchall()
        return rows


    @classmethod
    def get_address_in_range(cls, range, location):
        """Method to get the addresses within the given distance and location from DB
        """
        location = location.strip("(").strip(")").split(",")
        latitude = float(location[0].strip())
        longitude = float(location[1].strip())

        point= (latitude, longitude)

        addresses_within_range = list()
        all_addresses = cls.get_address()
        for address in all_addresses:
            address_point = [address[1], address[2]]

            distance_between_address_and_location = float(str(geodesic(location, address_point)).strip("km"))
            if distance_between_address_and_location <= range:
                addresses_within_range.append(address)
        
        return addresses_within_range


    def add_address(self):
        """Method to add/create a address in the DB
        """

        try:
            ids = Address.get_address_ids()
            if self.address_name in ids:
                return 1000
        except Exception as err:
            print(err)
    
        #Checking if the same location already exists
        if not self.validate_location():
            return 1001


        query = f""" INSERT INTO addresses VALUES
                ('{(self.address_name)}', {str(self.latitude)}, {str(self.longitude)})"""

        try:
            self.db_cursor.execute(query)
        except Exception as err:
            raise

        Address.db_commit()

        return True


    def update_address(self):
        """Method to update a address in the DB
        """
        try:
            ids = Address.get_address_ids()
            if self.address_name not in ids:
                return 1000
        except Exception as err:
            return 1003

        #Checking if the same location already exists
        if not self.validate_location():
            return 1001

        query = f"""
                    UPDATE addresses
                    SET LATITUDE = {self.latitude}, LONGITUDE = {self.longitude}
                    WHERE name = '{self.address_name}'
                """

        try:
            self.db_cursor.execute(query)
        except Exception as err:
            raise

        Address.db_commit()

        return True


    @classmethod
    def delete_address(cls, query_address_name):
        """Method to delete a address in the DB by name
        """
        ids = Address.get_address_ids()
        if query_address_name not in ids:
            return False

        query = f"""
                    DELETE FROM addresses WHERE name = '{query_address_name}'
                """
        try:
            cls.db_cursor.execute(query)
            Address.db_commit()
            return True
        except Exception as err:
            raise


    @classmethod
    def get_address_ids(cls):
        """Method to get all the address names present in the DB
        """
        cls.db_cursor.execute("""SELECT name FROM addresses""")
        rows = cls.db_cursor.fetchall()
        address_names = list(itertools.chain(*rows))
        return address_names


    def validate_location(self):
        """Method to validate the location by
           Rounding off the Lat, Long to 2 digits and check if the same combination already exists in database
        """
        query = f"""
                    SELECT * FROM addresses WHERE latitude = {self.latitude} AND longitude = {self.longitude}
                """
        self.db_cursor.execute(query)
        rows = self.db_cursor.fetchall()

        if rows:
            return False
        
        return True
