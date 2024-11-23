import psycopg2
from psycopg2.extras import execute_values
import random

import sql_queries as sq
from database import database 

database_instance = database('cp317_final2','heslip','pass123','localhost','5432')
conn, cur = database_instance.get_instance()

database_instance.delete_all()
database_instance.create_type_genre()

movies2 = [
    ["The Conjuring", "Horror", "Movie"],
    ["The Hobbit", "Fantasy, Adventure", "Movie"],
    ["Mad Max: Fury Road", "Action, Adventure", "Movie"],
    ["The Lord of the Rings: The Fellowship of the Ring", "Fantasy, Adventure", "Movie"],
    ["Titanic", "Romance, Drama", "Movie"],
    ["Won’t You Be My Neighbor?", "Documentary", "Movie"],
    ["The Shawshank Redemption", "Drama", "Movie"],
    ["The Dark Knight", "Action, Crime, Drama", "Movie"],
    ["The Matrix", "Sci-Fi, Action, Thriller", "Movie"],
    ["Inception", "Sci-Fi, Thriller", "Movie"],
    ["Schindler's List", "History, Drama", "Movie"],
    ["Frozen", "Animation, Adventure, Family", "Movie"],
    ["Saving Private Ryan", "War, Drama", "Movie"],
    ["Django Unchained", "Western, Drama, Action", "Movie"],
    ["A Nightmare on Elm Street", "Horror, Thriller", "Movie"],
    ["The Princess Bride", "Fantasy, Adventure, Romance", "Movie"],
    ["Gladiator", "Action, Drama", "Movie"],
    ["The Pursuit of Happyness", "Drama", "Movie"],
    ["Pulp Fiction", "Crime, Drama, Thriller", "Movie"],
    ["The Avengers", "Action, Adventure, Sci-Fi", "Movie"],
    ["Interstellar", "Sci-Fi, Adventure, Drama", "Movie"],
    ["Jaws", "Horror, Thriller", "Movie"],
    ["The Godfather", "Crime, Drama", "Movie"],
    ["The Revenant", "Adventure, Drama, Thriller", "Movie"],
    ["The Big Lebowski", "Comedy, Crime, Drama", "Movie"],
    ["The Silence of the Lambs", "Thriller, Crime, Drama", "Movie"],
    ["The Wizard of Oz", "Fantasy, Adventure, Family", "Movie"],
    ["Casablanca", "Romance, Drama, War", "Movie"],
    ["Star Wars: A New Hope", "Sci-Fi, Adventure, Action", "Movie"],
    ["Jurassic Park", "Adventure, Sci-Fi", "Movie"],
    ["Se7en", "Crime, Thriller", "Movie"],
    ["The Godfather Part II", "Crime, Drama", "Movie"],
    ["The Exorcist", "Horror, Thriller", "Movie"],
    ["12 Years a Slave", "Drama, History", "Movie"],
    ["The Great Gatsby", "Drama, Romance", "Movie"],
    ["The Green Mile", "Drama, Fantasy", "Movie"],
    ["The Social Network", "Drama, Biography", "Movie"],
    ["Forrest Gump", "Drama, Romance", "Movie"],
    ["The Hunger Games", "Adventure, Sci-Fi, Thriller", "Movie"],
    ["Star Wars: The Empire Strikes Back", "Sci-Fi, Adventure", "Movie"],
    ["The Truman Show", "Drama, Sci-Fi", "Movie"],
    ["The Terminator", "Action, Sci-Fi", "Movie"],
    ["The Expanse", "Sci-Fi, Thriller", "Movie"],
    ["The Hunger Games: Catching Fire", "Adventure, Sci-Fi, Thriller", "Movie"],
    ["The Matrix Reloaded", "Action, Sci-Fi", "Movie"],
    ["Inglourious Basterds", "War, Drama", "Movie"],
    ["The Dark Knight Rises", "Action, Drama, Thriller", "Movie"],
    ["Gladiator", "Action, Drama", "Movie"],
    ["The Shape of Water", "Fantasy, Drama, Romance", "Movie"],
    ["The Last Samurai", "War, Drama, Action", "Movie"],
    ["Moulin Rouge!", "Romance, Drama, Musical", "Movie"],
    ["The Thing", "Horror, Sci-Fi, Thriller", "Movie"],
    ["Doctor Strange", "Action, Adventure, Fantasy", "Movie"],
    ["The Pianist", "Drama, History", "Movie"],
    ["Gone with the Wind", "Drama, Romance, History", "Movie"],
    ["The Bridge on the River Kwai", "War, Drama", "Movie"],
    ["Heat", "Crime, Drama, Thriller", "Movie"],
    ["Into the Wild", "Adventure, Drama", "Movie"],
    ["Shutter Island", "Thriller, Mystery, Drama", "Movie"],
    ["The Good, the Bad, and the Ugly", "Western, Drama", "Movie"],
    ["American History X", "Drama, Crime", "Movie"],
    ["No Country for Old Men", "Crime, Drama, Thriller", "Movie"],
    ["The Big Short", "Drama, History", "Movie"],
    ["Schindler's List", "History, Drama", "Movie"],
    ["Black Swan", "Drama, Thriller", "Movie"],
    ["Pulp Fiction", "Crime, Drama, Thriller", "Movie"],
    ["Jurassic World", "Adventure, Action, Sci-Fi", "Movie"],
    ["Avatar", "Sci-Fi, Adventure, Action", "Movie"],
    ["Catch Me If You Can", "Drama, Biography", "Movie"],
    ["The Imitation Game", "Drama, History", "Movie"],
    ["The Great Escape", "Drama, War", "Movie"],
    ["The Departed", "Crime, Drama, Thriller", "Movie"],
    ["The Fault in Our Stars", "Romance, Drama", "Movie"],
    ["The Avengers: Endgame", "Action, Adventure, Sci-Fi", "Movie"],
    ["The Martian", "Sci-Fi, Drama, Adventure", "Movie"],
    ["The Shining", "Horror, Thriller", "Movie"],
    ["La La Land", "Romance, Drama, Musical", "Movie"],
    ["Citizen Kane", "Drama, Mystery", "Movie"],
    ["The Bourne Identity", "Action, Thriller, Mystery", "Movie"],
    ["The Godfather Part III", "Crime, Drama", "Movie"],
    ["Life is Beautiful", "Drama, Comedy, Romance", "Movie"],
    ["The Notebook", "Romance, Drama", "Movie"],
    ["The Revenant", "Adventure, Drama, Thriller", "Movie"],
    ["The Truman Show", "Drama, Comedy, Sci-Fi", "Movie"],
    ["The Lion King", "Animation, Adventure, Drama", "Movie"],
    ["A Beautiful Mind", "Drama, Biography", "Movie"],
    ["Prisoners", "Thriller, Crime, Drama", "Movie"],
    ["Madagascar", "Animation, Adventure, Comedy", "Movie"],
    ["The Croods", "Animation, Adventure, Comedy", "Movie"],
    ["Toy Story", "Animation, Adventure, Family", "Movie"],
    ["Finding Nemo", "Animation, Adventure, Family", "Movie"],
    ["Up", "Animation, Adventure, Comedy", "Movie"],
    ["Inside Out", "Animation, Adventure, Comedy", "Movie"],
    ["The Incredibles", "Animation, Action, Adventure", "Movie"],
    ["The Prestige", "Drama, Mystery, Sci-Fi", "Movie"],
    ["Whiplash", "Drama, Music", "Movie"],
    ["Blade Runner", "Sci-Fi, Thriller, Mystery", "Movie"],
    ["A Clockwork Orange", "Drama, Crime, Sci-Fi", "Movie"],
    ["The Grand Budapest Hotel", "Comedy, Drama", "Movie"],
    ["The Social Network", "Drama, Biography", "Movie"],
    ["The Wolf of Wall Street", "Drama, Comedy, Crime", "Movie"],
    ["Rocky", "Drama, Sport", "Movie"],
    ["The Godfather Part II", "Crime, Drama", "Movie"],
    ["Her", "Drama, Romance, Sci-Fi", "Movie"]
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

count_media = 104
max_reviews_per_account = 50

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
for account_id in account_ids:
    # Random number of movies to review for each account
    review_count = random.randint(1, max_reviews_per_account)
    
    # Select random movies to review
    selected_media_ids = random.sample(media_ids, review_count)

    for id in selected_media_ids:
        rating = random.randint(1, 10)
        # Insert the review for each selected movie
        cur.execute(sq.add_review_backend(), (account_id, id, rating, 'TESTING',))

conn.commit()
