from sql_functions import Database

db = Database()
tables = ["song_table", "artists", "time", "users", "songplays"]

def main():
    for table in tables:
        print(f"* Droping {table}")
        db.drop_table(table)

if __name__ == "__main__":
    main()
