import psycopg2
from psycopg2.extras import execute_values
import random

import sql_queries as sq
from database import database 

database_instance = database('cp317_final','heslip','GavinLeafs2003!','localhost','5432')
conn, cur = database_instance.get_instance()

database_instance.delete_all()
database_instance.create_type_genre()
movies = [
    ["The Shawshank Redemption", "Drama", "Movie"],
    ["The Godfather", "Crime", "Movie"],
    ["The Dark Knight", "Action", "Movie"],
    ["Pulp Fiction", "Crime", "Movie"],
    ["Forrest Gump", "Drama", "Movie"],
    ["Inception", "Sci-Fi", "Movie"],
    ["Fight Club", "Drama", "Movie"],
    ["The Matrix", "Action", "Movie"],
    ["Goodfellas", "Crime", "Movie"],
    ["The Lord of the Rings: The Fellowship of the Ring", "Fantasy", "Movie"],
    ["Star Wars: Episode V - The Empire Strikes Back", "Fantasy", "Movie"],
    ["The Silence of the Lambs", "Thriller", "Movie"],
    ["Schindler's List", "History", "Movie"],
    ["The Green Mile", "Drama", "Movie"],
    ["Gladiator", "Action", "Movie"],
    ["Interstellar", "Sci-Fi", "Movie"],
    ["The Lion King", "Animation", "Movie"],
    ["Saving Private Ryan", "War", "Movie"],
    ["The Departed", "Crime", "Movie"],
    ["Django Unchained", "Western", "Movie"]]

for movie in movies:
    cur.execute(sq.get_type(), (movie[2],))
    type = cur.fetchall()[0][0]
    cur.execute(sq.get_genre(), (movie[1],))
    genre = cur.fetchall()[0][0]
    date_released = "2069-01-10"
    studio = "TESTING"
    producer = "TESTING"
    name = movie[0]
    cur.execute(sq.add_media(), (type, genre, date_released,studio,producer,name,))
conn.commit()

