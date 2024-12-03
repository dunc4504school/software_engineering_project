import psycopg2
from psycopg2.extras import execute_values
import random
import sql_queries as sq
import pandas as pd
import unicodedata
from datetime import datetime, date


#Enter Command Line
#Run: "psql -U postgres"
#Enter your password
#Run: "CREATE DATABASE cp317_final"
#Run "\c cp317_final"
#Paste db.sql into terminal
#Run "SET CLIENT_ENCODING TO 'UTF8';"    #READ THIS!!!!!!!!!!!!!!!!!!!

conn = psycopg2.connect(
    host="localhost",
    database='cp317_db',
    user='heslip',   #Modify To Your User
    password='pass123',  #Modify To Your Password
    options="-c client_encoding=UTF8"
)
cur = conn.cursor()

cur.execute(sq.delete_all())


first_names = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", 
    "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica", 
    "Thomas", "Sarah", "Charles", "Karen", "Nelly", "Bobby", "Tyrone", "Lashanda"]

last_names = [
    "Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", 
    "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", 
    "Thompson", "Garcia", "Martinez", "Robinson", "Bobby", "McGorden", "Black", "Kappor"]

def setup_genres(row):

    #Storing Up To 3 Genres
    genres = eval(row['genres']) if row['genres'] != "[]" else []
    genre_ids = [None, None, None]
    genre_names = [None, None, None]

    #Getting Or Creating Their Corrasponding Ids
    if genres:
        for i, genre in enumerate(genres[:3]):  # Limit to 3 genres
            #Searching For Existing Match
            cur.execute(sq.get_genre(), (genre['name'],))
            result = cur.fetchone()

            #If Genre Already In DB
            if result:
                genre_ids[i] = result[0]

            #If Genre Is New (Add To DB)
            else:
                cur.execute(sq.add_genre(), (genre['name'],))
                conn.commit()
                result = cur.fetchone()
                genre_ids[i] = result[0]
    
    return genre_ids, genre_names

def setup_types(type):
    #Add type to the type table and retrieve its ID
    if type == "TV Movie":
        type_name = "Television"
    elif type == "Documentary":
        type_name = "Documentary"
    else:
        type_name = "Movie"
    
    cur.execute(sq.get_type(), (type_name,))
    result = cur.fetchone()

    #If Type Exists
    if result:                
        type_id = result[0]
    #Type Doesnt Exist
    else:
        cur.execute(sq.add_type(), (type_name,))
        conn.commit()                
        result = cur.fetchone()
        type_id = result[0]

    return type_id

def setup_accounts(accounts):

    for row in accounts.itertuples():
        fname = random.choice(first_names)
        lname = random.choice(last_names)
        user = f"{fname[0]}{lname}{random.randint(100, 999)}"
        date_to = date(2024, 10, random.randint(1,30))
        age = random.randint(18,24)
        
        cur.execute(sq.add_account_backend(), 
                    (f"{fname} {lname}", row.userId, user, date_to, "TEST", "TEST", "TEST", age))
    conn.commit()

def add_media(path):

    #Obtain Data
    data = pd.read_csv(path, compression="zip")

    #Cleaning Data
    data['title'] = data['title'].fillna(data['original_title'])
    data = data.where(pd.notnull(data), None)
    data.replace("nan", None, inplace=True)


    for _, row in data.iterrows():
        genre_ids, genre_names = setup_genres(row)

        type_id = setup_types(genre_names[0])
                    
        studios = eval(row['production_companies']) if row['production_companies'] != "[]" else []  # Safely handle empty studios
        if studios: first_studio_name = studios[0]['name']

    
        # Insert into the media table
        cur.execute(sq.add_media(), (
                    row['id'],
                    type_id,
                    genre_ids[0],  
                    genre_ids[1],
                    genre_ids[2],
                    row['release_date'],
                    first_studio_name, 
                    unicodedata.normalize("NFKC", row['title']),
                    row['vote_average'],
                    row['vote_count'],
                    row['overview'],
                    row['popularity'],
                    row['original_language'],
                    row['adult']
        ))
        conn.commit()
            
def add_review(path):

    data = pd.read_csv(path, compression="zip")
    data = data.dropna()

    data['userId'] = data['userId'].astype(int)
    data['movieId'] = data['movieId'].astype(int)


    accounts = data.groupby('userId')['timestamp'].min().reset_index()
    setup_accounts(accounts)

    for row in data.itertuples():
        date_to = date(2024, 11, random.randint(1,30))
        cur.execute(sq.add_review_backend(), 
                    (row.userId, row.movieId, row.rating, "TESTING", date_to, row.movieId, row.userId))
    conn.commit()

def add_testing(av):

    #Random Followings
    cur.execute(sq.setup_account_ids())
    account_ids = cur.fetchall()
    for index, account_id in enumerate(account_ids):

        follow_count = random.randint(1, av)
        account_ids_to_follow = random.sample(account_ids, follow_count)

        for follower_id in account_ids_to_follow:
            if follower_id == account_id: continue
            cur.execute(sq.add_following(), (account_id, follower_id))    
    conn.commit()  

    #Duplicate Name
    cur.execute("""UPDATE ACCOUNT set username = %s where id = 7""", ("movielover21",))
    conn.commit()
    #Demonstration Data Account
    cur.execute("""UPDATE ACCOUNT set name = %s, username = %s, date_created = %s, email = %s, phone = %s, password = %s
        WHERE id = %s""", ("John Testing", "JT123", "2024-11-01", "JT123@gmail.com", "9021101234", "password",6))
    conn.commit()
    #Add Reviews For Le Mis Of Friends (Might Break - Rerun)
    cur.execute(""" SELECT follows_id from following where account_id = %s""", (6,))
    follower_ids = cur.fetchall()
    cur.execute(sq.add_review_backend(), (follower_ids[0], 4415, 8.5, "TEST", "2024-11-07", 4415, follower_ids[0]))
    cur.execute(sq.add_review_backend(), (follower_ids[1], 4415, 9.7, "TEST", "2024-11-08", 4415, follower_ids[1]))
    cur.execute(sq.add_review_backend(), (follower_ids[2], 4415, 9.2, "TEST", "2024-11-12", 4415, follower_ids[2]))
    cur.execute(sq.add_review_backend(), (follower_ids[3], 4415, 8.9, "TEST", "2024-11-30", 4415, follower_ids[3]))
    #Setting "Silence Of The Lambs" to Adult For Easy Exampe
    cur.execute("UPDATE media set adult = TRUE where id = %s", (274,))
    conn.commit()





path = "movies_data.zip"
add_media(path)

path2 = "ratings_small.zip"
add_review(path2)


#Optional Slimming (removing non reviewed)
cur.execute(sq.slim_media())
conn.commit()

#Randomized Connections
add_testing(30)

