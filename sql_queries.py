
#Adds A Type: (Movie, Tv-Show)
def add_type():
    return """INSERT INTO type (name) VALUES (%s) returning id"""

#Adds A Genre: (Documentary, Action, Mystery)
def add_genre():
    return """INSERT INTO genre (name) VALUES (%s) returning id"""

#Adds Media
def add_media():
    return """INSERT INTO media(id,
                                type,
                                 genre,
                                 genre2,
                                 genre3,
                                 date_released,
                                 studio,
                                 name,
                                 full_average,
                                 total_reviews,
                                 description,
                                 popularity,
                                 language,
                                 adult) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
               ON CONFLICT (id) DO NOTHING;"""

def add_account_backend():
    return """INSERT INTO account(
                                  name, 
                                  id,
                                  username,
                                  date_created,
                                  email,
                                  phone,
                                  password,
                                  age)
              VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
              ON CONFLICT (username) DO NOTHING"""

#Adds Account
def add_account():
    return """INSERT INTO account(id,
                                 name, 
                                  username,
                                  date_created,
                                  email,
                                  phone,
                                  password)
              VALUES(%s, %s, %s, CURRENT_DATE, %s, %s, %s)
              ON CONFLICT (username) DO NOTHING"""

#Adds A Following: (account_id now follows follows_id)
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


def add_review_frontend():
    return """WITH new_review AS (
                INSERT INTO review (account_id, media_id, rating, description, date_reviewed)
                VALUES (%s, (SELECT id FROM media WHERE name = %s), %s, %s, CURRENT_DATE)
                RETURNING account_id, media_id, rating
              ), update_account AS (
                UPDATE account
                SET average_review = (
                    (average_review * total_reviews + (SELECT rating FROM new_review)) / (total_reviews + 1)
                ),
                average_expected = (
                    (average_expected * total_reviews + (SELECT full_average FROM media WHERE id = (SELECT media_id FROM new_review))) / (total_reviews + 1)
                ),
                total_reviews = total_reviews + 1
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


def add_review_backend():
    return """WITH new_review AS (
  INSERT INTO review (account_id, media_id, rating, description, date_reviewed)
  SELECT %s, %s, %s, %s, %s
  WHERE EXISTS (SELECT 1 FROM media WHERE id = %s)  -- Ensure media_id exists in media table
  AND EXISTS (SELECT 1 FROM account WHERE id = %s)  -- Ensure account_id exists in account table
  RETURNING account_id, media_id, rating
), update_account AS (
  UPDATE account
  SET average_review = (
      (average_review * total_reviews + (SELECT rating FROM new_review)) / (total_reviews + 1)
  ),
  average_expected = (
      (average_expected * total_reviews + (SELECT full_average FROM media WHERE id = (SELECT media_id FROM new_review))) / (total_reviews + 1)
  ),
  total_reviews = total_reviews + 1
  WHERE id = (SELECT account_id FROM new_review)
  RETURNING id
)
UPDATE media
SET total_reviews = total_reviews + 1,
    full_average = (
        (full_average * total_reviews + (SELECT rating FROM new_review)) 
        / (total_reviews + 1)
    )
WHERE id = (SELECT media_id FROM new_review);
   """
#     return """WITH new_review AS (
#   INSERT INTO review (account_id, media_id, rating, description, date_reviewed)
#   SELECT %s, %s, %s, %s, %s
#   WHERE EXISTS (SELECT 1 FROM media WHERE id = %s)  -- Only insert if media_id exists in media
#   RETURNING account_id, media_id, rating
# ), update_account AS (
#   UPDATE account
#   SET average_review = (
#       (average_review * total_reviews + (SELECT rating FROM new_review)) / (total_reviews + 1)
#   ),
#   average_expected = (
#       (average_expected * total_reviews + (SELECT full_average FROM media WHERE id = (SELECT media_id FROM new_review))) / (total_reviews + 1)
#   ),
#   total_reviews = total_reviews + 1
#   WHERE id = (SELECT account_id FROM new_review)
#   RETURNING id
# )
# UPDATE media
# SET total_reviews = total_reviews + 1,
#     full_average = (
#         (full_average * total_reviews + (SELECT rating FROM new_review)) 
#         / (total_reviews + 1)
#     )
# WHERE id = (SELECT media_id FROM new_review);

    
    
#     """
    
    
    
#     """ WITH new_review AS (
#   INSERT INTO review (account_id, media_id, rating, description, date_reviewed)
#   VALUES (%s, %s, %s, %s, %s)
#   ON CONFLICT (media_id) DO NOTHING 
#   RETURNING account_id, media_id, rating
# ), update_account AS (
#   UPDATE account
#   SET average_review = (
#       (average_review * total_reviews + (SELECT rating FROM new_review)) / (total_reviews + 1)
#   ),
#   average_expected = (
#       (average_expected * total_reviews + (SELECT full_average FROM media WHERE id = (SELECT media_id FROM new_review))) / (total_reviews + 1)
#   ),
#   total_reviews = total_reviews + 1
#   WHERE id = (SELECT account_id FROM new_review)
#   RETURNING id
# )
# UPDATE media
# SET total_reviews = total_reviews + 1,
#     full_average = (
#         (full_average * total_reviews + (SELECT rating FROM new_review)) 
#         / (total_reviews + 1)
#     )
# WHERE id = (SELECT media_id FROM new_review) """



    # return """WITH new_review AS (
    #             INSERT INTO review (account_id, media_id, rating, description, date_reviewed)
    #             VALUES (%s, %s, %s, %s, %s)
    #             RETURNING account_id, media_id, rating
    #           ), update_account AS (
    #             UPDATE account
    #             SET average_review = (
    #                 (average_review * total_reviews + (SELECT rating FROM new_review)) / (total_reviews + 1)
    #             ),
    #             average_expected = (
    #                 (average_expected * total_reviews + (SELECT full_average FROM media WHERE id = (SELECT media_id FROM new_review))) / (total_reviews + 1)
    #             ),
    #             total_reviews = total_reviews + 1
    #             WHERE id = (SELECT account_id FROM new_review)
    #             RETURNING id
    #         )
    #         UPDATE media
    #         SET total_reviews = total_reviews + 1,
    #         full_average = (
    #             (full_average * total_reviews + (SELECT rating FROM new_review)) 
    #             / (total_reviews + 1)
    #         )
    #         WHERE id = (SELECT media_id FROM new_review);"""





#----------------------------------------------------------------------------------------

#Deletes A Following: (account_id not DOESNT follow follow_id)
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

#-----------------------------------------------------------------------------------------------

#Returns Type Id Given Name
def get_type():
    return """ SELECT id from type where name = %s """

#Returns Genre Id Given Name
def get_genre():
    return """ SELECT id from genre where name = %s"""

#Returns {limit} number random media
def get_random_media(limit):
    return f""" SELECT id from media ORDER BY total_reviews DESC LIMIT {limit}"""

#Returns Account Id Given Username
def get_matching_account():
    return """SELECT id from account where username = %s"""


#Returns List Of Accounts With Similar Usernames
def get_searched_account():
    return f"""SELECT id, 
                    name, 
                    username, 
                    (SELECT 1 from following where account_id = %s and follows_id = id) 
            FROM ACCOUNT
            WHERE LOWER(name) LIKE %s     
            """

#Returns List Of Media With Similar Names
def get_searched_media():
    return """SELECT id,
                     name,
                     type,
                     genre,
                     genre2,
                     genre3,
                     date_released,
                     studio,
                     producer,
                     full_average,
                     total_reviews
              FROM MEDIA
              WHERE name LIKE %s
    """

#Returns media given id
def get_media():
    return """SELECT id,
                     name,
                     type,
                     genre,
                     genre2,
                     genre3,
                     date_released,
                     studio,
                     producer,
                     full_average,
                     total_reviews
              FROM MEDIA
              WHERE id = %s
    """

# Returns media with the names of each genre
def get_media_genre_names():
    return """SELECT media.id, 
                    media.name, 
                    type.name AS type,
                    genre.name AS genre, 
                    genre2.name AS genre2, 
                    genre3.name AS genre3,
                    media.date_released, 
                    media.full_average, 
                    media.total_reviews,
                    media.studio,
                    media.producer,
                    media.description,
                    media.popularity,
                    media.language,
                    adult
            FROM media
            JOIN type ON media.type = type.id
            LEFT JOIN genre AS genre ON media.genre = genre.id
            LEFT JOIN genre AS genre2 ON media.genre2 = genre2.id
            LEFT JOIN genre AS genre3 ON media.genre3 = genre3.id
            WHERE media.id = %s
        """

#Returns a summary of account (for anouther persons accout)
def get_account_summary():
    return f"""SELECT id, 
                    name, 
                    username, 
                    total_reviews, 
                    total_followers,
                    total_following,
                    average_review,
                    average_review - average_expected,
                    date_created
            FROM ACCOUNT
            WHERE id = %s     
            """
#Returns a summary of account (for your account)
def get_self_summary():
    return """SELECT id, 
                    name, 
                    username,
                    phone,
                    email, 
                    total_reviews, 
                    total_followers,
                    total_following,
                    date_created,
                    average_review,
                    average_review - average_expected,
                    age
            FROM ACCOUNT
            WHERE id = %s     
            """

#Returns Account Info, if username and password match some record
def attempt_login():
    return """
            SELECT id from account 
            WHERE username = %s AND
            password = %s
            """

#Returns the list of reviews made by an account
def get_account_review():
    return """
        SELECT m.name,
            r.rating, 
            r.rating - m.full_average As Delta,
            r.description, 
            CONCAT_WS(', ', g.name, g2.name, g3.name) AS genres,  
            t.name AS type_name,
            m.id,
            r.date_reviewed
        FROM review r
        JOIN media m ON r.media_id = m.id
        LEFT JOIN genre g ON m.genre = g.id
        LEFT JOIN genre g2 ON m.genre2 = g2.id
        LEFT JOIN genre g3 ON m.genre3 = g3.id   
        LEFT JOIN type t ON m.type = t.id    
        WHERE r.account_id = %s
        ORDER BY r.date_reviewed DESC;
        """

def get_media_reviews():
    return """
            SELECT 
    r.rating, 
    r.date_reviewed, 
    a.username, 
    r.rating - m.full_average AS rating_delta,
    a.id
FROM 
    review r
JOIN 
    account a ON r.account_id = a.id
JOIN 
    media m ON r.media_id = m.id
WHERE 
    r.media_id = %s
    AND EXISTS (
        SELECT 1 
        FROM following 
        WHERE account_id = %s 
        AND follows_id = a.id
    )
ORDER BY 
    r.date_reviewed DESC
LIMIT 10;
            
        """

#Returns the list of account that follow this account
def get_account_follows():
    return """
    SELECT a.id, a.name, a.username, f.date_followed
    FROM following f
    JOIN account a on f.account_id = a.id
    WHERE f.follows_id = %s
    ORDER BY f.date_followed DESC;"""

#Returns the list of acccounts that this account is following
def get_account_following():
    return  """
    SELECT a.id, a.name, a.username, f.date_followed 
    FROM following f
    JOIN account a ON f.follows_id = a.id
    WHERE f.account_id = %s
    ORDER BY f.date_followed DESC;"""


#Returns The Most Recent Reviews Made By People This Account Follows
def get_account_recent():
    return """
    SELECT DISTINCT ON (a.id) 
           t.name AS type_name,
           g.name AS genre_name,
           g2.name AS genre2_name,
           g3.name AS genre3_name,
           m.name AS media_name,
           a.name AS account_name,
           r.rating,
           r.rating - m.full_average AS rating_difference,
           r.description,
           r.date_reviewed
    FROM review r
    JOIN account a ON r.account_id = a.id
    JOIN media m ON r.media_id = m.id
    JOIN genre g ON m.genre = g.id
    JOIN genre g2 ON m.genre2 = g2.id
    JOIN genre g3 ON m.genre3 = g3.id  
    JOIN type t ON m.type = t.id   
    WHERE a.id IN (
        SELECT follows_id
        FROM following
        WHERE account_id = %s
    )
    ORDER BY a.id, r.date_reviewed DESC  
    LIMIT 10;
    """

# Returns movie objects the meet the criteria requested by the user
def search_movies_by_attributes():
    return """
        SELECT media.id, media.name, type.name AS type,
            COALESCE(genre.name, '') || 
            CASE WHEN genre2.name IS NOT NULL THEN ', ' || genre2.name ELSE '' END ||
            CASE WHEN genre3.name IS NOT NULL THEN ', ' || genre3.name ELSE '' END AS genres,
            media.date_released
        FROM media
        JOIN type ON media.type = type.id
        LEFT JOIN genre ON media.genre = genre.id
        LEFT JOIN genre AS genre2 ON media.genre2 = genre2.id
        LEFT JOIN genre AS genre3 ON media.genre3 = genre3.id
        WHERE 
            LOWER(media.name) LIKE %s OR
            LOWER(type.name) LIKE %s OR
            LOWER(genre.name) LIKE %s OR
            LOWER(genre2.name) LIKE %s OR
            LOWER(genre3.name) LIKE %s OR
            TO_CHAR(media.date_released, 'YYYY-MM-DD') LIKE %s
        GROUP BY media.id, media.name, type.name, media.date_released, genre.name, genre2.name, genre3.name
    """

# Returns all accounts
def get_all_accounts():
    return """
        SELECT *
        FROM account;
    """
# Returns 5 most recently made reviews
def get_recent_reviews():
    return """
            SELECT r.description, r.rating, r.date_reviewed, m.name
            FROM review r
            JOIN media m ON r.media_id = m.id
            WHERE r.account_id = %s
            ORDER BY r.date_reviewed desc
            LIMIT 5;
        """ 

# Returns 5 most recent reviews for a specific movie



def delete_all():
        return """
            DELETE from following;
            DELETE from review;
            DELETE from account;
            DELETE from media;
            DELETE from type;
            DELETE from genre;
        """


def reccomendations():
    return """WITH FollowedReviews AS (
    SELECT 
        r.media_id,
        AVG(r.rating) AS avg_rating_from_followed
    FROM 
        following f
    JOIN 
        review r ON f.follows_id = r.account_id
    WHERE 
        f.account_id = %s
    GROUP BY 
        r.media_id
)
SELECT 
    m.id,
    m.name AS media_name,
    m.full_average,
    COALESCE(fr.avg_rating_from_followed, 0) AS avg_rating_from_followed,
    (POWER(m.full_average, 1.2) + POWER(COALESCE(fr.avg_rating_from_followed, 0),1.2)) AS total_score
FROM 
    media m
LEFT JOIN 
    FollowedReviews fr ON m.id = fr.media_id
WHERE 
    m.type = %s 
    AND (m.genre = %s OR m.genre2 = %s OR m.genre3 = %s) 
    AND avg_rating_from_followed > 0
ORDER BY 
    total_score DESC; """     


def slim_media():
    return """
        DELETE FROM media
        WHERE NOT EXISTS (
            SELECT 1 
            FROM review 
            WHERE review.media_id = media.id
        );
    """


def setup_account_ids():
    return """
        SELECT id
        from account;
    
    """
