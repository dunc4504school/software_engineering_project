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
#Run "SET CLIENT_ENCODING TO 'UTF8';"    #READ THIS!!!!!!!!!!!!!!!!!!!

conn = psycopg2.connect(
    host="localhost",
    database='cp317_db',
    user='postgres',   #Modify To Your User
    password='password',  #Modify To Your Password
    options="-c client_encoding=UTF8"
)
cur = conn.cursor()

cur.execute(sq.delete_all())



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
                    row['vote_count']
        ))
        conn.commit()
            

        

def add_testing():

    testing_users = [
    ('Venkat Gunturi', 'Venn123'),
    ('Gavin Heslip', 'Chislm'),
    ('Hashim Jama', 'HJ1324'),
    ('Zach Reid', 'BigTarra432_x'),
    ('Lucas Duncan', 'PenUlty'),
    ('Emily Carter', 'EmC123'),
    ('Michael Nguyen', 'MikeN77'),
    ('Sophia Patel', 'Sophie_P_21'),
    ('Liam Brown', 'LiamBr_009'),
    ('Olivia Smith', 'LivS2022'),
    ('Noah Wilson', 'NoahWils90'),
    ('Ava Johnson', 'AvaJ98x'),
    ('Ethan Martinez', 'E_Martz_56'),
    ('Mia Hernandez', 'MiaH45'),
    ('Jacob Lee', 'JakeL_1234'),
    ('Isabella Garcia', 'IzzyG88'),
    ('William Anderson', 'WillA_22'),
    ('Charlotte Moore', 'CharM007'),
    ('James Thomas', 'JT99Rocks'),
    ('Amelia Hall', 'AmyH_91'),
    ('Benjamin Young', 'BenjiY19'),
    ('Emma Scott', 'EmmaS23'),
    ('Alexander Adams', 'AlexAdams_88'),
    ('Ella Baker', 'EllaB07'),
    ('Henry Walker', 'HWalker'),
    ('Grace Lewis', 'GraceL98'),
    ('Lucas Ramirez', 'LucaRam12'),
    ('Mason Clark', 'MClarkX'),
    ('Lily Turner', 'LilyT567'),
    ('Elijah Rivera', 'EliR2020'),
    ('Abigail Torres', 'AbbyT'),
    ('Oliver Bennett', 'OBennett77'),
    ('Chloe Stewart', 'ChloeS32'),
    ('Logan Foster', 'LoganF_22'),
    ('Sophia Hughes', 'SophH99'),
    ('Jackson Perry', 'JackP88'),
    ('Harper Price', 'HPrice42'),
    ('Gabriel Morales', 'GabeMor123')]
    account_ids = []
    for account in testing_users:
        cur.execute(sq.add_account(), (account[0],account[1],'TEST', 'TEST', 'TEST'))
        cur.execute(sq.get_matching_account(), (account[1],))
        account_ids.append(cur.fetchone())
    conn.commit()

    #Creating Followings
    for account_id in account_ids:
        follow_count = random.randint(1, len(account_ids) - 1)
        account_ids_to_follow = random.sample(account_ids, follow_count)
        for follower_id in account_ids_to_follow:
            if follower_id == account_id: continue
            cur.execute(sq.add_following(), (account_id, follower_id))
    conn.commit()  

    #Sample Media
    cur.execute(sq.get_random_media(100))
    media_ids = cur.fetchall()

    #Creating Reviews
    for media_id in media_ids:
        review_count = random.randint(1, len(account_ids)-1)
        account_ids_to_review = random.sample(account_ids, review_count)

        for account_id_to_review in account_ids_to_review:
            rating = random.randint(1, 10)
            cur.execute(sq.add_review_backend(), (account_id_to_review, media_id, rating, 'TESTING',))
        conn.commit()


path = "movies_data.zip"
add_media(path)

#ADD REVIEWS HERE

add_testing()