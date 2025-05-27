# imports
from helper import helper
from db_operations import db_operations

# global variables
db_ops = db_operations("playlist.db")

# functions
def startScreen():
    print("Welcome to your playlist!")
    #db_ops.create_songs_table()
    db_ops.populate_songs_table("songs.csv")

# show user menu options
def options():
    print('''Select from the following menu options:
    1. Find songs by artist
    2. Find songs by genre
    3. Find songs by feature
    4. Update song information
    5. Remove song from playlist
    6. Exit''')
    return helper.get_choice([1,2,3,4,5,6])

def search_by_artist():
    # get list of all artists in table
    query = '''
    SELECT DISTINCT Artist
    FROM songs;
    '''
    print("Artists in playlist: ")
    artists = db_ops.single_attribute(query)

    # show all artists, create dictionary of options, and let user choose
    choices = {}
    for i in range(len(artists)):
        print(i, artists[i])
        choices[i] = artists[i]
    index = helper.get_choice(choices.keys())

    # user can ask to see 1, 5, or all songs
    print("How many songs do you want returned for", choices[index]+"?")
    print("Enter 1, 5, or 0 for all songs")
    num = helper.get_choice([1, 5, 0])

    # print results
    query = '''SELECT DISTINCT name
    FROM songs
    WHERE Artist =:artist ORDER BY RANDOM()
    '''
    dictionary = {"artist":choices[index]}
    if num != 0:
        query += "LIMIT:lim"
        dictionary["lim"] = num
    results = db_ops.single_attribute_params(query, dictionary)
    helper.pretty_print(results)


def search_by_feature():
    # features we want to search by
    features = ['Danceability', 'Liveness', 'Loudness']
    choices = {}

    # show all features in table and create dictionary
    choices = {}
    for i in range(len(features)):
        print(i, features[i])
        choices[i] = features[i]
    index = helper.get_choice(choices.keys())

    # user can ask to see 1, 5, or all songs
    print("How many songs do you want returned for", choices[index]+"?")
    print("Enter 1, 5, or 0 for all songs")
    num = helper.get_choice([1, 5, 0])

    # what order does the user want this returned in?
    print("Do you want results sorted in asc or desc order?")
    order = input("ASC or DESC: ")

    # print results
    query = "SELECT DISTINCT name FROM songs ORDER BY "+choices[index]+" "+order
    dictionary = {}
    if num != 0:
        query += " LIMIT:lim"
        dictionary["lim"] = num
    results = db_ops.single_attribute_params(query, dictionary)
    helper.pretty_print(results)

# search for songs by genre
def search_by_genre():
    # get list of genres
    query = '''
    SELECT DISTINCT Genre
    FROM songs;
    '''
    print("Genres in playlist:")
    genres = db_ops.single_attribute(query)

    # show genres in table and create dictionary
    choices = {}
    for i in range(len(genres)):
        print(i, genres[i])
        choices[i] = genres[i]
    index = helper.get_choice(choices.keys())

    # user can ask to see 1, 5, or all songs
    print("How many songs do you want returned for", choices[index]+"?")
    print("Enter 1, 5, or 0 for all songs")
    num = helper.get_choice([1, 5, 0])

    # print results
    query = '''SELECT DISTINCT name
    FROM songs
    WHERE Genre =:genre ORDER BY RANDOM()
    '''
    dictionary = {"genre":choices[index]}
    if num != 0:
        query += "LIMIT:lim"
        dictionary["lim"] = num
    results = db_ops.single_attribute_params(query, dictionary)
    helper.pretty_print(results)

# SONG UPDATE INFORMATION
def update_song():
    song_to_update = input("Enter the name of the song you would like to update:\n")
    song_to_update_query = "SELECT songID FROM songs WHERE Name = \""+song_to_update+"\" LIMIT 1"
    song_to_update_ID = db_ops.single_record(song_to_update_query)
    query2 = "SELECT * FROM songs WHERE songID = \""+song_to_update_ID+"\" LIMIT 1"
    song_attributes = db_ops.select_query(query2)

    helper.pretty_print(song_attributes)
    
    attribute_to_update = 0
    while (attribute_to_update not in [1,2,3,4,5]):
        attribute_to_update = int(input("Which attribute would you like to modify?\n"
                                        + "(Select a number 1-5)\n"
                                        + "1: Name\n"
                                        + "2: Artist\n"
                                        + "3: Album\n"
                                        + "4: Release Date\n"
                                        + "5: Explicit\n"))
        if attribute_to_update not in [1,2,3,4,5]:
            print("invalid input :(\n")

    success = False
    while (success == False):
            if attribute_to_update == 1:
                new = input("What would you like the new Name to be?\n")
                if isinstance(new, str) and len(new) <= 20:
                    name_query = "UPDATE songs SET Name = \""+new+"\" WHERE songID = \""+song_to_update_ID+"\""
                    db_ops.modify_query(name_query)
                    success = True
                else:
                    print("Incorrect value, try again")
            elif attribute_to_update == 2:
                new = input("What would you like the new Artist to be?\n")
                if isinstance(new, str) and len(new) <= 20:
                    artist_query = "UPDATE songs SET Artist = \""+new+"\" WHERE songID = \""+song_to_update_ID+"\""
                    db_ops.modify_query(artist_query)
                    success = True
                else:
                    print("Incorrect value, try again")
            elif attribute_to_update == 3:
                new = input("What would you like the new Album to be?\n")
                if isinstance(new, str) and len(new) <= 20:
                    album_query = "UPDATE songs SET Album = \""+new+"\" WHERE songID = \""+song_to_update_ID+"\""
                    db_ops.modify_query(album_query)
                    success = True
                else:
                    print("Incorrect value, try again")
            elif attribute_to_update == 4:
                new = input("What would you like the new Release Date to be?\n")
                failed = False
                if len(new) != 10:
                    failed = True
                else:
                    for i in range(len(new)):
                        if i == 4 or i == 7:
                            if new[i] != '-':
                                failed = True
                        else:
                            try:
                                int(new[i])
                            except:
                                failed = True
                if failed == False:
                    date_query = "UPDATE songs SET releaseDate = \""+new+"\" WHERE songID = \""+song_to_update_ID+"\""
                    db_ops.modify_query(date_query)
                    success = True
                else:
                    print("Incorrect value, try again")
            elif attribute_to_update == 5:
                new = input("What would you like the new Explicit to be?\n")
                if new.lower() == "true" or new.lower() == "false":
                    ex_query = "UPDATE songs SET Explicit = \""+new+"\" WHERE songID = \""+song_to_update_ID+"\""
                    db_ops.modify_query(ex_query)
                    success = True
                else:
                  print("Incorrect value, try again")  

# SONG DELETION
def remove_song():
    song_to_delete = input("What is the name of the song you would like to remove?\n")
    query = "SELECT songID FROM songs WHERE Name = \""+song_to_delete+"\" LIMIT 1"
    song_to_delete_ID = db_ops.single_record(query)
    delete_query = "DELETE FROM songs WHERE songID = \""+song_to_delete_ID+"\""
    db_ops.modify_query(delete_query)

# main method
startScreen()

# NEW DATA UPDATE
new_songs = input("Would you like to load new songs onto the data base? (yes/no)\n")
if new_songs.lower() == "yes":
    new_songs_path = input("What is the location of the file containing the new songs?\n")
    db_ops.insert_new_songs(new_songs_path)
else:
    print("Continuing with current songs..")

# program loop
while True:
    user_choice = options()
    if user_choice == 1:
        search_by_artist()
    if user_choice == 2:
        search_by_genre()
    if user_choice == 3:
        search_by_feature()
    if user_choice == 4:
        update_song()
    if user_choice == 5:
        remove_song()
    if user_choice == 6:
        print("Goodbye!")
        break

db_ops.destructor()
