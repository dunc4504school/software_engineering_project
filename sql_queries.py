def add_type():
    return """INSERT INTO type (name) VALUES (%s)"""

def add_genre():
    return """INSERT INTO genre (name) VALUES (%s)"""

def add_media():
    return """INSERT INTO media(type,
                                 genre,
                                 date_released,
                                 studio,
                                 producer,
                                 name) 
               VALUES (%s, %s, %s, %s, %s, %s)"""

def add_account():
    return """INSERT INTO account(name, 
                                  username,
                                  date_created,
                                  email,
                                  phone,
                                  password)
              VALUES(%s, %s, CURRENT_DATE, %s, %s, %s)
              ON CONFLICT (username) DO NOTHING"""

def add_following():
    return """WITH new_follow AS (
                INSERT INTO following (account_id, follows_id, date_followed)
                VALUES (%s, %s, CURRENT_DATE)
                RETURNING account_id, follows_id
              ),update_following AS (
                UPDATE account
                SET total_following = total_following + 1
                WHERE id = (SELECT account_id FROM new_follow)
                RETURNING id
              )
             UPDATE account
             SET total_followers = total_followers + 1
             WHERE id = (SELECT follows_id FROM new_follow);"""

def delete_following():
    return """WITH deleted_follow AS (
    DELETE FROM following
    WHERE account_id = %s AND follows_id = %s
    RETURNING account_id, follows_id
    ), update_following AS (
    UPDATE account
    SET total_following = total_following - 1
    WHERE id = (SELECT account_id FROM deleted_follow)
    RETURNING id
    )
    UPDATE account
    SET total_followers = total_followers - 1
    WHERE id = (SELECT follows_id FROM deleted_follow);  
    """



def add_review():
    return """WITH new_review AS (
                INSERT INTO review (account_id, media_id, rating, description, date_reviewed)
                VALUES (%s, %s, %s, %s, CURRENT_DATE)
                RETURNING account_id, media_id, rating
              ), update_account AS (
                UPDATE account
                SET total_reviews = total_reviews + 1
                WHERE id = (SELECT account_id FROM new_review)
                RETURNING id
            )
            UPDATE media
            SET total_reviews = total_reviews + 1,
            full_average = (
                (full_average * total_reviews + (SELECT rating FROM new_review)) 
                / (total_reviews + 1)
            )
            WHERE id = (SELECT media_id FROM new_review);"""


def get_type():
    return """ SELECT id from type where name = %s """

def get_genre():
    return """ SELECT id from genre where name = %s"""

def get_random_media(limit):
    return f""" SELECT id from media ORDER BY RANDOM() LIMIT {limit}"""

def get_matching_account():
    return """SELECT id from account where username = %s"""

def get_searched_account():
    return f"""SELECT id, 
                    name, 
                    username, 
                    total_reviews, 
                    total_followers,
                    total_following,
                    (Select AVG(rating) from review where account_id = id)
            FROM ACCOUNT
            WHERE username LIKE %s     
            """

def get_searched_media():
    return """SELECT id,
                     name,
                     type,
                     genre,
                     date_released,
                     studio,
                     producer,
                     full_average,
                     total_reviews
              FROM MEDIA
              WHERE name LIKE %s
    """

def get_account_summary():
    return f"""SELECT id, 
                    name, 
                    username, 
                    total_reviews, 
                    total_followers,
                    total_following,
                    (Select AVG(rating) from review where account_id = id)
            FROM ACCOUNT
            WHERE id = %s     
            """

def get_self_summary():
    return """SELECT id, 
                    name, 
                    username,
                    phone,
                    email, 
                    total_reviews, 
                    total_followers,
                    total_following,
                    (Select AVG(rating) from review where account_id = id)
            FROM ACCOUNT
            WHERE id = %s     
            """

def attempt_login():
    return """
            SELECT * from account 
            WHERE username = %s AND
            password = %s
            """

def get_account_review():
    return """
        SELECT m.name,
       r.rating, 
       r.rating - m.full_average,
       r.description, 
       g.name AS genre_name,  
       t.name AS type_name    
        FROM review r
        JOIN media m ON r.media_id = m.id
        LEFT JOIN review orr ON orr.media_id = r.media_id
        LEFT JOIN genre g ON m.genre = g.id   
        LEFT JOIN type t ON m.type = t.id    
        WHERE r.account_id = %s
        GROUP BY r.media_id, r.rating, r.description, m.name, m.full_average, g.name, t.name;
    """

def get_account_follows():
    return """
    SELECT a.id, a.name, a.total_reviews, a.total_following, a.total_followers 
    FROM following f
    JOIN account a on f.account_id = a.id
    WHERE f.follows_id = %s;"""

def get_account_following():
    return  """
    SELECT a.id, a.name, a.total_reviews, a.total_following, a.total_followers 
    FROM following f
    JOIN account a ON f.follows_id = a.id
    WHERE f.account_id = %s;"""


def get_account_recent():
    return """
    SELECT t.name AS type_name,
       g.name AS genre_name,
       m.name AS media_name,
       a.name AS account_name,
       r.rating,
       r.rating - m.full_average AS rating_difference,
       r.description
    FROM review r
    JOIN account a ON r.account_id = a.id
    JOIN media m ON r.media_id = m.id
    JOIN genre g ON m.genre = g.id  
    JOIN type t ON m.type = t.id   
    WHERE a.id IN (
        SELECT follows_id
        FROM following
        WHERE account_id = %s
    )
    ORDER BY r.date_reviewed DESC  
    LIMIT 20;
    """



