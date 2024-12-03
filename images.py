import sql_queries as sq 
import pandas as pd

def download_poster(downloaded_image_dir, title, label, poster_path):
    import os
    import re
    import requests
    import time
    
    if not os.path.exists(downloaded_image_dir):
        os.makedirs(downloaded_image_dir)
        
    if not os.path.exists(downloaded_image_dir+'/'+label):
        os.makedirs(downloaded_image_dir+'/'+label)

    imgUrl = 'http://image.tmdb.org/t/p/w185' + poster_path

    local_filename = re.sub(r'\W+', ' ', title).lower().strip().replace(" ", "-") + '.jpg'

    try:
        session = requests.Session()
        r = session.get(imgUrl, stream=True, verify=False)
        with open(downloaded_image_dir+'/'+label+'/'+local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)
    except Exception as e:
        print('Problem downloading:', title, label, poster_path, imgUrl, "\nError:", e)
    
    time.sleep(1)


def add_media(path, downloaded_image_dir):
    # Obtain Data
    data = pd.read_csv(path, compression="zip")

    # Cleaning Data
    data['title'] = data['title'].fillna(data['original_title'])
    data = data.where(pd.notnull(data), None)
    data.replace("nan", None, inplace=True)

    for _, row in data.iterrows():
        genre_ids, genre_names = sq.setup_genres(row)

        type_id = sq.setup_types(genre_names[0])

        studios = eval(row['production_companies']) if row['production_companies'] != "[]" else []  # Safely handle empty studios
        first_studio_name = studios[0]['name'] if studios else None

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

        # Download poster for the media
        if row['poster_path']:
            download_poster(
                downloaded_image_dir=downloaded_image_dir,
                title=row['title'],
                label=genre_names[0] if genre_names[0] else "Unknown",
                poster_path=row['poster_path']
            )

poster_directory = "downloaded_posters"
path = "movies_data.zip"
sq.add_media(path, poster_directory)