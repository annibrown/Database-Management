# imports
from helper import helper
from db_operations import db_operations

# global variables
db_ops = db_operations("ride_share.db")

# functions
def start_screen():
    print("Welcome to Ride Share!")
    #db_ops.create_rides_table()
    #db_ops.create_riders_table()
    #db_ops.create_drivers_table()
    db_ops.populate_rides_table("rides.csv")
    db_ops.populate_riders_table("riders.csv")
    db_ops.populate_drivers_table("drivers.csv")

# show user menu options
def options():
    print('''Which are you?
            1. New User
            2. Rider
            3. Driver
            4. Exit''')
    return helper.get_choice([1,2,3,4])

def driverMenu():
    # Ask for ID number to log in
    print("What is your ID number?")
    driverID = input("ID Number: ")

    # Check to see if ID number is valid and log in
    IDvalidity = db_ops.check_driverID(driverID)

    # Depending on if ID is valid or not, either exits to main menu or repeats Driver functions until Driver exits the app
    if IDvalidity:
        while True:
            driver_choice = driver_options()
            if driver_choice == 1:
                view_driver_rating(driverID)
            if driver_choice == 2:
                view_driver_rides(driverID)
            if driver_choice == 3:
                update_driver_mode(driverID)
            if driver_choice == 4:
                print("Goodbye!")
                break
    else:
        print("Not a valid ID number. Try logging in with a valid one.")

# menu options for driver account
def driver_options():
    print('''What would you like to do?
            1. View Rating
            2. View Rides
            3. Activate / Deactivate Driver Mode
            4. Sign Out''')
    return helper.get_choice([1,2,3,4])

# driver choice functions
def view_driver_rating(id):
    #query that returns average rating with given ID
    query = """
    SELECT AVG(rating)
    FROM rides
    WHERE driverID = {}
    """.format(
        id
    )

    #prints current rating to user
    rating = db_ops.single_record(query)
    print("Your Current Rating: ")
    print(rating)

def view_driver_rides(id):
    # return all records of rides where driverID = id
    query = f'''
    SELECT *
    FROM rides
    WHERE driverID LIKE "{id}";
    '''
    results = db_ops.select_query(query)
    print("Here is a list of all rides you have given:\n")
    helper.pretty_print(results)

def update_driver_mode(id):
    print('''What would you like your driver mode to be?
          1. Activated (ready to accept ride requests)
          2. Deactivated (not ready to accept ride requests)''')
    mode_choice = helper.get_choice([1,2])
    if mode_choice == 1:
        mode_bool = True
    elif mode_choice == 2:
        mode_bool = False
    query = f'''
        UPDATE drivers
        SET driverMode = "{mode_bool}"
        WHERE driverID = "{id}";
        '''
    db_ops.modify_query(query)
    print("Driver mode updated!\n")

    # displays driver's info to make sure it updated
    query = f'''
    SELECT *
    FROM drivers
    WHERE driverID LIKE "{id}";
    '''
    results = db_ops.select_query(query)
    helper.pretty_print(results)

def riderMenu():
    #asks for ID number to log in
    print("What is your ID number?")
    riderID = input("ID Number: ")

    #check to see if ID number is valid and log in...
    IDvalidity = db_ops.check_riderID(riderID)

    #depending on if ID is valid or not, either exits to main menu or repeats Rider functions until Rider exits the app
    if IDvalidity:
        while True:
            print(
                """
            Would you like to:
                1. View rides
                2. Find a driver
                3. Rate my driver
                4. Sign out
            """
            )
            #ensures error-checking for options
            riderChoice = helper.get_choice([1, 2, 3, 4])

            #ensures functionality for each of the Rider options (viewing rides, finding driver, rating driver, or exiting)
            if riderChoice == 1:
                riderViewRides(riderID)
            if riderChoice == 2:
                findADriver(riderID)
            if riderChoice == 3:
                rateDriver(riderID)
            if riderChoice == 4:
                break
    else:
        print("Not a valid ID number. Try logging in with a valid one.")

# function to view each of the rides the logged in Rider has
def riderViewRides(ID):
    # query statement to get all rides that the rider has taken
    queryOfRides = f"""
    SELECT *
    FROM rides
    WHERE riderID = '{ID}';
    """
    # queries the database and pretty(ish) prints the rides for the rider
    print("Here is your list of rides:")
    print(
        "(rideID, driverID, riderID, rating, dropOffLocation, pickUpLocation, price, tipAmount)"
    )
    rides = db_ops.select_query(queryOfRides)
    for i, ride in enumerate(rides):
        print(f"Ride {i + 1}: {ride}")

#function that finds a random driver for the logged in Rider
def findADriver(ID):
    # Query that finds random driver with driver mode activated
    query = """
    SELECT driverName
    FROM drivers
    WHERE driverMode = 'true'
    ORDER BY RANDOM()
    LIMIT 1
    """

    # Returns random driver and prints confirmation of matched driver to user
    driver = db_ops.single_record(query)
    print("You have been matched with " + driver + "!")

    # Gathers information to store in a new Ride entry
    print("Please provide the following: ")
    pickup = input("Pick-up Location: ")
    dropoff = input("Drop-off Location: ")

    # Gets driverID from driver name
    name_query = """
    SELECT driverID
    FROM drivers
    WHERE driverName = '{}'
    """.format(driver)
    driverID = db_ops.single_record(name_query)

    # Initially sets rating to 0/NULL until updated
    rating = 0

    # Inserts new record for the ride into the rides table
    new_ride_query = """
    INSERT INTO rides (driverID, riderID, rating, dropOffLocation, pickUpLocation)
    VALUES (?, ?, ?, ?, ?)
    """
    db_ops.modify_query_params(new_ride_query, (driverID, ID, rating, dropoff, pickup))

    # Informs user of successful ride entry
    print(f"Successfully created a ride for Rider {ID} with Driver {driver}.")

#FIX
#function to rate the driver of logged in Rider's most recent ride
def rateDriver(riderID):
    #query statement to get all rides that the rider has taken
    queryOfRides = """
    SELECT *
    FROM rides
    WHERE riderID = '{}'
    ORDER BY rideID DESC;
    """.format(
        riderID
    )

    #list of all of the rides that the rider has taken in order of most recent to least recent
    allOfRidersRides = db_ops.select_query(queryOfRides)

    #first ride result from the sorted list (most recent ride)
    recentRide = allOfRidersRides[0]

    #rideID from the most recent ride
    correctRideID = recentRide[0]

    #pretty(ish) prints the most recent ride to the rider
    print("Here is your most recent ride:")
    print(
        "(rideID, driverID, riderID, rating, dropOffLocation, pickUpLocation, price, tipAmount)"
    )
    print()
    helper.pretty_print([recentRide])

    #prompts rider if the displayed ride is correct
    correctRideUserInput = input("Is this correct? (Type 'Yes' or 'No'): ")
    print()

    #if the ride displayed is NOT the intended ride the rider wishes to see
    while correctRideUserInput.lower() == "no":

        #prompts rider for the correct rideID of the ride the rider wishes to see
        correctRideID = input(
            "Please input the correct Ride ID of the ride you'd like to rate: "
        )

        #query statement for getting the correct ride
        queryOfCorrectRide = """
        SELECT *
        FROM rides
        WHERE rideID = '{}';
        """.format(
            correctRideID
        )

        #correct ride attributes
        correctRecentRide = db_ops.select_query(queryOfCorrectRide)[0]

        #pretty(ish) prints the correct ride the rider wishes to see
        print("Here is your most recent ride:")
        print("(driverId, riderID, rating, dropOffLocation, pickUpLocation, price, tipAmount)")
        print()
        helper.pretty_print([correctRecentRide])

        #reprompts user if the displayed ride is correct
        correctRideUserInput = input("Is this correct? (Type 'Yes' or 'No'): ")
        print()

    #if the ride is the correct ride the rider wishes to see
    if correctRideUserInput.lower() == "yes":

        #prompt rider for ride rating
        inputRating = input("Please input a rating from 1 to 5: ")
        print()

        #query statement to chaneg ride rating
        updateRatingQuery = """
        UPDATE rides
        SET rating = '{}'
        WHERE rideID = '{}';
        """.format(
            inputRating, correctRideID
        )

        #queries the database to change the ride rating
        db_ops.modify_query(updateRatingQuery)
        print("You have successfully rated your ride!")

    return

def newUserOptions():
    print('''What type of account would you like to create?
        1. Rider
        2. Driver''')
    new_account = helper.get_choice([1,2])
    new_name = input("Please enter your name:\n")
    if new_account == 1:
        db_ops.create_new_rider(new_name)
        print("Your rider ID is: " + str(db_ops.get_rider_id(new_name)))
    if new_account == 2:
        db_ops.create_new_driver(new_name)
        print("Your driver ID is: " + str(db_ops.get_driver_id(new_name)))

# main method
start_screen()

#while loop that loops through main menu until user chooses to exit
while True:
    user_choice = options()
    if user_choice == 1:
        newUserOptions()
    if user_choice == 2:
        riderMenu()
    if user_choice == 3:
        driverMenu()
    if user_choice == 4:
        print("Exiting RideShare App...")
        break
    
db_ops.destructor()
