# import library
import sqlite3
print('import')

# add path to chinook.db to connect to it
connection = sqlite3.connect("chinook.db")
print('connection: ', connection)

# cursor object that excecutes SQL commands
cur_obj = connection.cursor()
print('init cursor: ', cur_obj)

# always close connections when exiting
cur_obj.close()
connection.close()
print('connection closed')

def createQuery():
    # query to create the table tweet
    create_query = '''
    CREATE TABLE tweet(
        tweetID INTEGER NOT NULL PRIMARY KEY,
        Text VARCHAR(280),
        creationDate DATETIME,
        User VARCHAR(20),
        Likes INTEGER,
        Retweets INTEGER,
        Comments INTEGER
    );
    '''
    # execute query using cursor object
    cur_obj.execute(create_query)

    # commit modification made to database
    connection.commit()
    print('Tweet Table Successfully Created')

def insertQueryHardCode():
    # query to insert a record (hard coded values)
    insert_query = '''
    INSERT INTO tweet
    VALUES(1, 'This is a tweet', '2022-01-01', "@Sarah", 1, 2, 3);
    '''
    # execute, commit, print confirmation
    # put executes and commits in try/except
    cur_obj.execute(insert_query)
    connection.commit()
    print('Inserted hard coded values successfully')

def insertQueryQmark():
    # A tuple with 4 values to be inserted
    record = (2, 'This is not a tweet', '2021-01-02', '@Alice')

    # insert query with q-mark placeholders
    insert_query = '''
    INSERT INTO tweet(tweetID, Text, creationDate, User)
    VALUES (?,?,?,?)
    '''
    # in execute function, pass query and tuple to fill in
    cur_obj.execute(insert_query, record)
    connection.commit()

def insertManyQuery():
    # a list of tuples to be added
    records = [(3, 'hello world', '2021-01-03', '@Eve'),
               (4, 'hello universe', '2021-01-04', '@Bob'),
               (5, 'this is patrick', '2021-01-05', '@Star')]
    
    # insert query with q-mark placeholders
    insert_query = '''
    INSERT INTO tweet(tweetID, Text, creationDate, User)
    VALUES (?,?,?,?)
    '''

    # use executemany function for multiple records
    cur_obj.executemany(insert_query, records)
    connection.commit()

def insertExecuteScriptQuery():
    # many insert queries in a row
    insert_queries = '''
    INSERT INTO tweet(tweetID, Text, creationDate, User)
    VALUES (6, 'hello', '2022-02-02', '@Sarah');
    INSERT INTO tweet(tweetID, Text, creationDate, User)
    VALUES (7, 'hello!!!!!', "2021-01-06', '@skwillz');
    '''

    # use executemany function for multiple records
    cur_obj.executescript(insert_queries)
    connection.commit()

def updateQuery():
    # New likes, comments, retweets, tweetID data
    new_data = [(4, 5, 10, 2),
                (10, 15, 20, 3),
                (500000, 0, 1, 5)]
    
    # Update query with placeholders for respective VALUES
    update_query = '''
    UPDATE tweet
    SET Likes = ?, Comments = ?, Retweets = ?
    WHERE tweetID = ?
    '''

    # execute many and commit
    cur_obj.executemany(update_query, new_data)
    connection.commit()

# written by prof instead of selectQuery
def selectStatement():
    select = '''
                SELECT * 
                FROM tweet 
                WHERE Likes = 10000;
            '''
    result = cur_obj.execute(select)
    connection.commit()

def selectQuery():
    # select query
    select_query = '''
    SELECT *
    FROM tweet;
    '''

    # store returned records into a result object
    result = cur_obj.execute(select_query)

    # iterate through result and print
    for row in result:
        print(row)

def selectQueryFetchOne():
    # select query
    select_query = '''
    SELECT *
    FROM tweet;
    '''

    # store returned records into a result object
    result = cur_obj.execute(select_query)

    # fetchone() will return records from execution
    # one by one whenever called
    print(result.fetchone())
    print(result.fetchone())

def selectQueryFetchAll():
    # select query
    select_query = '''
    SELECT *
    FROM tweet;
    '''

    # store returned records into a result object
    result = cur_obj.execute(select_query)

    # fetchall() will return all records FROM
    # previous execution as a list of tuples
    for row in result.fetchall():
        print(row)

def selectQueryPlaceholder():
    # name to fetch results for
    search_name = '@Star'

    # select query with name as a placeholder
    select_query = '''
    SELECT *
    FROM tweet
    WHERE User = '%s'
    '''

    # passing search_name using pything string functions
    result = cur_obj.execute(select_query % search_name)

    # print results
    for row in result:
        print(row)

def selectQueryQmarkPlaceholder():
    #name to fetch results for
    search_name = ['@pStar']

    #using qmark placeholder
    select_query = '''
    SELECT *
    FROM tweet
    WHERE User = ?;
    '''

    #passing search_name as a tuple
    result = cur_obj.execute(select_query, search_name)
    #print results
    for row in result:
        print(row)

def selectQueryNamedPlaceholder():
    #name and ID to fetch results
    name = '@Clibourne'
    id = 1
    #using named placeholder
    select_query = '''
    SELECT *
    FROM tweet
    WHERE User = :username
    AND tweetID = :tID;
    '''
    #passing parameters as a dictionary
    result = cur_obj.execute(select_query,{'username':name, 'tID':id})
    #print results
    for row in result:
        print(row)

def insertQueryInnocentTweet():
    #an innocent tweet being inserted
    text = 'Another tweet'

    #use a string placeholder for text
    update_query = '''
    INSERT INTO tweet(tweetID, Text) VALUES (20, '%s');
    ''' % text

    #executescript helps show us this example
    cur_obj.executescript(update_query)
    connection.commit()

def insertQuerySQLInjection():
    #SQL Injection to drop astronaut table
    text = 'Another tweet\');DROP TABLE astronaut;--'

    #use a string placeholder for text
    update_query = '''
    INSERT INTO tweet(tweetID, Text) VALUES (21, '%s');
    ''' % text

    #executescript helps show us this example
    cur_obj.executescript(update_query)
    connection.commit()

def insertQuerySafe():
    #SQL Injection to drop astronaut table
    text = 'Another tweet\');DROP TABLE astronaut;--'

    #sanitize our inputs before inserting
    text = sanitize_input(text)

    #use a string placeholder for text
    update_query = '''
    INSERT INTO tweet(tweetID, Text) VALUES (22, '%s');
    ''' % text

    #executescript helps show us this example
    cur_obj.executescript(update_query)
    connection.commit()

def sanitize_input(user_input):
    # Remove harmful characters
    no_colons = user_input.replace(';', '')
    no_single_quotes = no_colons.replace("'", "''")
    no_backslash = no_single_quotes.replace("\\", '')
    sanitized_input = no_backslash.replace("--", '')
    return sanitized_input


#main method

#createQuery()
#insertQueryHardCode()
#insertQueryQmark()
#insertManyQuery()
#insertExecuteScriptQuery()
#updateQuery()
#selectQuery()
#selectQueryFetchOne()
#selectQueryFetchAll()
#selectQueryPlaceholder()
#selectQueryQmarkPlaceholder()
#selectQueryNamedPlaceholder()
#insertQueryInnocentTweet()
#insertQuerySQLInjection
#insertQuerySafe()

#always close connections when exiting
cur_obj.close()
connection.close()
print('connection closed')
