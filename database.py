import psycopg2
import sql_queries as sq


class database:



    def __init__(self, dbname,user,password,host,port):
        self.conn = psycopg2.connect(dbname=dbname,
                                    user=user,
                                    password=password,
                                    host=host,
                                    port=port)
        self.cur = self.conn.cursor()

    def get_instance(self):
        return self.conn, self.cur



    def delete_all(self):
        self.cur.execute("""
            DELETE from following;
            DELETE from review;
            DELETE from account;
            DELETE from media;
            DELETE from type;
            DELETE from genre;
        """)
        self.conn.commit()


    def create_type_genre(self):
        types = ['Movie', 'Tv-Show']
        self.cur.executemany(sq.add_type(), [(type,) for type in types])

        genres = ['Horror', 'Fantasy', 'Action', 'Adventure', 'Romance', 'Documentary', 
          'Drama', 'Crime', 'Sci-Fi', 'Thriller', 'History', 'Animation', 'War', 'Western']    
        self.cur.executemany(sq.add_genre(), [(genre,) for genre in genres])
        
        self.conn.commit()       