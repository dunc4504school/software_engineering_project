import psycopg2
from psycopg2.extras import execute_values
import random

import sql_queries as sq
from database import database 

database_instance = database('cp317_final','heslip','GavinLeafs2003!','localhost','5432')
conn, cur = database_instance.get_instance()

database_instance.delete_all()
database_instance.create_type_genre()

movies2 = [
    ["Gladiator", "Action", "Movie"],
    ["Interstellar", "Sci-Fi, Adventure, Drama", "Movie"],
    ["The Lion King", "Animation, Adventure", "Movie"],
    ["Saving Private Ryan", "War, Drama", "Movie"],
    ["The Departed", "Crime, Drama, Thriller", "Movie"],
    ["Django Unchained", "Western, Drama, Action", "Movie"],
    ["Inception", "Sci-Fi, Thriller", "Movie"],
    ["The Dark Knight", "Action, Crime, Drama", "Movie"],
    ["The Avengers", "Action, Adventure, Sci-Fi", "Movie"],
    ["The Godfather", "Crime", "Movie"]
]

# Loop through movies
for movie in movies2:
    cur.execute(sq.get_type(), (movie[2],))  # Get type_id based on the type (e.g., 'Movie')
    type_id = cur.fetchone()[0]

    # Prepare a list of genre IDs
    genre_ids = []
    for genre_name in movie[1].split(","):  # Split the genres by commas
        genre_name = genre_name.strip()  # Remove leading/trailing spaces from the genre name
        cur.execute(sq.get_genre(), (genre_name,))
        result = cur.fetchone()

        if result:  # If genre exists, fetch the genre_id
            genre_id = result[0]
        else:
            # If genre doesn't exist, insert the genre into the genre table
            cur.execute("INSERT INTO genre (name) VALUES (%s) RETURNING id", (genre_name,))
            genre_id = cur.fetchone()[0]  # Fetch the newly inserted genre_id

        genre_ids.append(genre_id)

    # Ensure there are 3 genres (even if fewer, set to None/NULL)
    while len(genre_ids) < 3:
        genre_ids.append(None)

    # Insert into the media table with 3 genres
    cur.execute(sq.add_media(), (type_id, genre_ids[0], genre_ids[1], genre_ids[2], "2069-01-10", "TESTING", "TESTING", movie[0]))

# Commit changes to the database
conn.commit()

#Sample Real Account (Used For Presentation)

count_media = 50
max_reviews_per_account = 10

#Adding Account Names
account_names = ['Venkat Gunturi', 'Gavin Heslip', 'Hashim Jama', 
                 'Zach Reid', 'Lucas Duncan', 'John Doe', 'Jane Smith',
                 'Kylie Tan', 'Bertha Blue', 'Tiffany Stoik']

cur.executemany(sq.add_account(), [(account,"TESTING" + account, "TESTING" + account, "TESTING", "TESTING" ) for account in account_names])
conn.commit()

#Sample media
cur.execute(sq.get_random_media(count_media))
media_ids = cur.fetchall()

#Sample Account Ids
account_ids = []
for name in account_names:
    cur.execute(sq.get_matching_account(), ("TESTING" + name,))
    account_ids.append(cur.fetchall()[0][0])


#Create Sample Followings
for id in account_ids:
    follow_count = random.randint(1, len(account_ids) - 1)
    account_ids_to_follow = random.sample(account_ids, follow_count)
    for follower_id in account_ids_to_follow:
        if follower_id == id: continue
        cur.execute(sq.add_following(), (id, follower_id))
conn.commit()  

#Create Sample Reviews:
for id in media_ids:
    review_count = random.randint(1, max_reviews_per_account)
    
    account_ids_to_review = random.sample(account_ids, review_count)

    for account_id in account_ids_to_review:
        rating = random.randint(1, 10)
        cur.execute(sq.add_review(), (account_id, id, rating, 'TESTING',))
conn.commit()
