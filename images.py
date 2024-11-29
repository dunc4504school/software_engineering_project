import requests
import time
import re
import os

def download_poster(downloaded_image_dir, title, label, poster_path):
  
    if not os.path.exists(downloaded_image_dir):
        os.makedirs(downloaded_image_dir)
        
    if not os.path.exists(downloaded_image_dir+'/'+label):
        os.makedirs(downloaded_image_dir+'/'+label)

    imgUrl = 'http://image.tmdb.org/t/p/w185/' + poster_path

    local_filename = re.sub(r'\W+', ' ', title).lower().strip().replace(" ", "-") + '.jpg'

    try:
        session = requests.Session()
        r = session.get(imgUrl, stream=True, verify=False)
        with open(downloaded_image_dir+'/'+label+'/'+local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)
    except:
        print('PROBLEM downloading', title,label,poster_path,imgUrl)
    
    time.sleep(1)
