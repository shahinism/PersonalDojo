from sql_functions import Database


def main():
    db = Database()

    print("* Create song_table")
    db.create_table(
        "song_table",
        "song_id varchar, title varchar, artist_id varchar, year integer, duration decimal, PRIMARY KEY(song_id)",
    )

    print("* Create artists")
    db.create_table(
        "artists",
        "artist_id varchar PRIMARY KEY, name varchar, location varchar, latitude float(7), longitude float(7)",
    )

    print("* Create time")
    db.create_table(
        "time",
        "start_time bigint PRIMARY KEY, hour int, day int, week int, month int, year int, weekday int",
    )

    print("* Create users")
    db.create_table(
        "users",
        "user_id INT PRIMARY KEY, first_name varchar, last_name varchar, gender varchar, level varchar",
    )

    print("* Create songplays")
    db.create_table(
        "songplays",
        "songplay_id SERIAL PRIMARY KEY, start_time bigint NOT NULL, user_id int NOT NULL, level varchar, song_id varchar, artist_id varchar, session_id int, location varchar, user_agent varchar",
    )


if __name__ == "__main__":
    main()
