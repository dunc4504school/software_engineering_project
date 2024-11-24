import psycopg2
from psycopg2.extras import execute_values
import random
import sql_queries as sq
import pandas as pd
import unicodedata


#Enter Command Line
#Run: "psql -U postgres"
#Enter your password
#Run: "CREATE DATABASE cp317_final"
#Run "\c cp317_final"
#Paste db.sql into terminal
#Run "SET CLIENT_ENCODING TO 'UTF8';"

conn = psycopg2.connect(
    host="localhost",
    database='cp317_db',
    user='postgres',   #Modify To Your User
    password='password',  #Modify To Your Password
    options="-c client_encoding=UTF8"
)
cur = conn.cursor()

cur.execute(sq.delete_all())

path = "movies_data.zip"

#Obtain Data
data = pd.read_csv(path, compression="zip")

#Cleaning Data
data['title'] = data['title'].fillna(data['original_title'])
data = data.where(pd.notnull(data), None)
data.replace("nan", None, inplace=True)
    
serial = 0

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

try:
    
    for _, row in data.iterrows():

        genre_ids, genre_names = setup_genres(row)

        type_id = setup_types(genre_names[0])
                    
        studios = eval(row['production_companies']) if row['production_companies'] != "[]" else []  # Safely handle empty studios
        if studios: first_studio_name = studios[0]['name']

        # Insert into the media table
        cur.execute(sq.add_media(), (
                    type_id,
                    genre_ids[0],  
                    genre_ids[1],
                    genre_ids[2],
                    row['release_date'],
                    first_studio_name, 
                    unicodedata.normalize("NFKC", row['title']),
                    row['vote_average'],
                    row['vote_count']
        ))
                
        print("Row " + str(serial) + " inserted.")
        serial +=1
        conn.commit()
except Exception as e:
    conn.rollback()
    print("Error inserting data:", e)
    print("Problematic row: ")
    raise

