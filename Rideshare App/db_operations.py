import sqlite3
from helper import helper

class db_operations():
    # constructor with connection path to DB
    def __init__(self, conn_path):
        self.connection = sqlite3.connect(conn_path)
        self.cursor = self.connection.cursor()
        print("connection made..")

    # function to simply execute a DDL or DML query.
    # commits query, returns no results. 
    # best used for insert/update/delete queries with no parameters
    def modify_query(self, query):
        self.cursor.execute(query)
        self.connection.commit()

    # function to simply execute a DDL or DML query with parameters
    # commits query, returns no results. 
    # best used for insert/update/delete queries with named placeholders
    def modify_query_params(self, query, dictionary):
        self.cursor.execute(query, dictionary)
        self.connection.commit()

    # function to simply execute a DQL query
    # does not commit, returns results
    # best used for select queries with no parameters
    def select_query(self, query):
        result = self.cursor.execute(query)
        return result.fetchall()
    
    # function to simply execute a DQL query with parameters
    # does not commit, returns results
    # best used for select queries with named placeholders
    def select_query_params(self, query, dictionary):
        result = self.cursor.execute(query, dictionary)
        return result.fetchall()

    # function to return the value of the first row's 
    # first attribute of some select query.
    # best used for querying a single aggregate select 
    # query with no parameters
    def single_record(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]
    
    # function to return the value of the first row's 
    # first attribute of some select query.
    # best used for querying a single aggregate select 
    # query with named placeholders
    def single_record_params(self, query, dictionary):
        self.cursor.execute(query, dictionary)
        return self.cursor.fetchone()[0]
    
    # function to return a single attribute for all records 
    # from some table.
    # best used for select statements with no parameters
    def single_attribute(self, query):
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        results = [i[0] for i in results]
        results.remove(None)
        return results
    
    # function to return a single attribute for all records 
    # from some table.
    # best used for select statements with named placeholders
    def single_attribute_params(self, query, dictionary):
        self.cursor.execute(query,dictionary)
        results = self.cursor.fetchall()
        results = [i[0] for i in results]
        return results
    
    # function for bulk inserting records
    # best used for inserting many records with parameters
    def bulk_insert(self, query, data):
        self.cursor.executemany(query, data)
        self.connection.commit()
    
    # function that creates riders table in our database
    def create_riders_table(self):
        query = '''
        CREATE TABLE riders(
            riderID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            riderName VARCHAR(20)
        );
        '''
        self.cursor.execute(query)
        print('Riders table Created')


    # function that creates drivers table in our database
    def create_drivers_table(self):
        query = '''
        CREATE TABLE drivers(
            driverID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            driverName VARCHAR(20),
            driverRating DOUBLE,
            driverMode BOOL
        );
        '''
        self.cursor.execute(query)
        print('Drivers table Created')

    # function that creates rides table in our database
    def create_rides_table(self):
        query = '''
        CREATE TABLE rides(
            rideID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            driverID INT,
            riderID INT,
            rating DOUBLE,
            dropOffLocation VARCHAR(20),
            pickUpLocation VARCHAR(20),
            price DOUBLE,
            tipAmount DOUBLE,
            FOREIGN KEY (driverID) REFERENCES drivers(driverID),
            FOREIGN KEY (riderID) REFERENCES riders(riderID)
        );
        '''
        self.cursor.execute(query)
        print('Rides table Created')

    # function that returns if riders table has records
    def is_riders_empty(self):
        #query to get count of riders in table
        query = '''
        SELECT COUNT(*)
        FROM riders;
        '''
        #run query and return value
        result = self.single_record(query)
        return result == 0

    # function that returns if drivers table has records
    def is_drivers_empty(self):
        #query to get count of drivers in table
        query = '''
        SELECT COUNT(*)
        FROM drivers;
        '''
        #run query and return value
        result = self.single_record(query)
        return result == 0

    # function that returns if rides table has records
    def is_rides_empty(self):
        #query to get count of rides in table
        query = '''
        SELECT COUNT(*)
        FROM rides;
        '''
        #run query and return value
        result = self.single_record(query)
        return result == 0

    # function to populate riders table given some path
    # to a CSV containing records
    def populate_riders_table(self, filepath):
        if self.is_riders_empty():
            data = helper.data_cleaner(filepath)
            attribute_count = len(data[0])
            placeholders = ("?,"*attribute_count)[:-1]
            query = "INSERT INTO riders (riderName) VALUES("+placeholders+")"
            self.bulk_insert(query, data)

    # function to populate riders table given some path
    # to a CSV containing records
    def populate_drivers_table(self, filepath):
        if self.is_drivers_empty():
            data = helper.data_cleaner(filepath)
            attribute_count = len(data[0])
            placeholders = ("?,"*attribute_count)[:-1]
            query = "INSERT INTO drivers (driverName, driverRating, driverMode) VALUES("+placeholders+")"
            self.bulk_insert(query, data)

    # function to populate songs table given some path
    # to a CSV containing records
    def populate_rides_table(self, filepath):
        if self.is_rides_empty():
            data = helper.data_cleaner(filepath)
            attribute_count = len(data[0])
            placeholders = ("?,"*attribute_count)[:-1]
            query = "INSERT INTO rides (driverID, riderID, rating, dropOffLocation, pickUpLocation, price, tipAmount) VALUES (" + placeholders + ")"
            self.bulk_insert(query, data)

    #adds a new rider to the game with the name riderName
    def create_new_rider(self, riderName):
        query = "INSERT INTO riders (riderName) VALUES(?)"
        self.cursor.execute(query, (riderName,))

    #adds a new driver to the game with the name driverName
    def create_new_driver(self, driverName):
        query = "INSERT INTO drivers (driverName, driverRating, driverMode) VALUES(?, NULL, false)"
        self.cursor.execute(query, (driverName, ))

    #returns riderID based on riderName
    def get_rider_id(self, riderName):
        query = f'''
        SELECT riderID
        FROM riders
        WHERE riderName LIKE "{riderName}";
        '''
        return self.single_record(query)

    #returns driverID based on driverName
    def get_driver_id(self, driverName):
        query = f'''
        SELECT driverID
        FROM drivers
        WHERE driverName LIKE "{driverName}";
        '''
        return self.single_record(query)
    
    #function that returns true/false depending on whether a certain driver ID already exists in Driver database
    def check_driverID(self, ID):
        #query to see if database has a Driver with given ID
            query = '''
            SELECT COUNT(*)
            FROM drivers
            WHERE driverID = {}
            '''.format(ID)

            #run query and returns true/false value given equivalency to a 0 count
            #returns true if no records, returns false if there is a record (kinda opposite logic, I know, but it works)
            result = self.single_record(query)
            return result > 0
    
    #function that returns true/false depending on whether a certain rider ID already exists in Rider database
    def check_riderID(self, ID):
        #query to see if database has a rider with given ID
            query = '''
            SELECT COUNT(*)
            FROM riders
            WHERE RiderID = {}
            '''.format(ID)

            #run query and returns true/false value given equivalency to a 0 count
            result = self.single_record(query)
            return result != 0

    # destructor that closes connection with DB
    def destructor(self):
        self.cursor.close()
        self.connection.close()
