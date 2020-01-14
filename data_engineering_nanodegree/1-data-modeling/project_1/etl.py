import glob
import os

import pandas as pd
import psycopg2
from sql_functions import *


def process_song_file(db, filepath):
    """
    Processes song file from song_data directory to create two tables: song_data and artist_data
    Args:
    - db: Allows to run Postgres command
    - filepath: File to be processed and extracted to Postgres tables

    Returns:
    None
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[["song_id", "title", "artist_id", "year", "duration"]].values[0]
    # print(len(song_data))
    db.execute_query(song_table_insert, song_data)

    # insert artist record
    artist_data = df[
        [
            "artist_id",
            "artist_name",
            "artist_location",
            "artist_latitude",
            "artist_longitude",
        ]
    ].values[0]
    db.execute_query(artist_table_insert, artist_data)


def process_log_file(db, filepath):
    """
    Processes log file from log_data directory to create three tables: time, users, and songplays

    Args:
    - db: Allows to run Postgres command
    - filepath: File to be processed and extracted to Postgres tables

    Returns: None
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df.page == "NextSong"]

    # convert timestamp column to datetime
    t = pd.to_datetime(df["ts"] / 1000, unit="s")

    # insert time data records
    time_data = dict(
        timestamp=df.ts,
        hour=t.dt.hour.values,
        day=t.dt.day.values,
        weekofyear=t.dt.weekofyear.values,
        month=t.dt.month.values,
        year=t.dt.year.values,
        weekday=t.dt.weekday.values,
    )
    time_data = pd.DataFrame(data=time_data)
    time_df = pd.DataFrame(data=time_data)

    for i, row in time_df.iterrows():
        db.execute_query(time_table_insert, list(row))

    # load user table
    user_df = df[["userId", "firstName", "lastName", "gender", "level"]]

    # insert user records
    for i, row in user_df.iterrows():
        db.execute_query(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():

        # get songid and artistid from song and artist tables
        db.execute_query(song_select, (row.song, row.artist, row.length))
        results = db.cur.fetchone()

        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (
            row.ts,
            row.userId,
            row.level,
            songid,
            artistid,
            row.sessionId,
            row.location,
            row.userAgent,
        )
        db.execute_query(songplay_table_insert, songplay_data)


def process_data(db, filepath, func):
    """
    Process all the files in data directory and creates Postgres tables

    Args:
        - db: Allows to run Postgres command
        - filepath: File to be processed and extracted to Postgres tables
        - func: Function to be allowed for ETL, can take two values
            + process_song_data: when filepath is song_data, or
            + process_log_data: when filepath is log_data

    Returns:
    None
    """

    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, "*.json"))
        for f in files:
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print("{} files found in {}".format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(db, datafile)
        print("{}/{} files processed.".format(i, num_files))


def main():
    # connect to Postgress database
    # create a database helper to run SQL queries
    db = Database()

    # process song_data directory
    process_data(db, filepath="data/song_data", func=process_song_file)

    # process log_data directory
    process_data(db, filepath="data/log_data", func=process_log_file)

    db.close()


if __name__ == "__main__":
    main()
