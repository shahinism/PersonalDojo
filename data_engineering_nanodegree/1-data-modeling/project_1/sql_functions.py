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
