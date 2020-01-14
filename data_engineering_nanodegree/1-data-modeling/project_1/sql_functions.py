import psycopg2


class Database:
    def __init__(
        self,
        host="127.0.0.1",
        dbname="udacity_de",
        user="postgres",
        password="postgres",
    ):
        self.__conn = psycopg2.connect(
            host=host, dbname=dbname, user=user, password=password
        )
        self.__conn.set_session(autocommit=True)
        self.cur = self.__conn.cursor()

    def execute_query(self, *args, error=None, **kwargs):
        try:
            self.cur.execute(*args, **kwargs)
        except psycopg2.Error as e:
            if error:
                print(error)
            print(e)

    def drop_table(self, name):
        self.execute_query(
            f"DROP TABLE IF EXISTS {name}", error="Error: dropping table"
        )

    def create_table(self, name, fields_desc):
        self.execute_query(
            f"CREATE TABLE IF NOT EXISTS {name} ({fields_desc})",
            error="Error: Issue creating table",
        )

    def print_query(self, query):
        self.execute_query(query)
        for row in self.cur.fetchall():
            print(row)

    def print_table(self, name):
        self.print_query(f"SELECT * FROM {name}")

    def close(self):
        self.__conn.close()


song_table_insert = """
INSERT INTO song_table
       (song_id, title, artist_id, year, duration)
       VALUES (%s, %s, %s, %s, %s)
       ON CONFLICT (song_id) DO NOTHING
"""

artist_table_insert = """
INSERT INTO artists
       (artist_id, name, location, latitude, longitude)
       VALUES (%s, %s, %s, %s, %s)
       ON CONFLICT (artist_id) DO NOTHING
"""

time_table_insert = """
INSERT INTO TIME
       (start_time, hour, day, week, month, year, weekday)
       VALUES (%s, %s, %s, %s, %s, %s, %s)
       ON CONFLICT (start_time) DO NOTHING
"""

user_table_insert = """
INSERT INTO users
       (user_id, first_name, last_name, gender, level)
       VALUES (%s, %s, %s, %s, %s)
       ON CONFLICT (user_id) DO NOTHING
"""

song_select = """
SELECT song_id, a.artist_id
FROM song_table AS s
JOIN artists AS a
ON a.artist_id = s.artist_id
WHERE s.title = (%s)
AND a.name = (%s)
AND s.duration = (%s)
"""
