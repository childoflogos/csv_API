import psycopg2

class Database:
    def __init__(self):
        print('Connecting to the PostgreSQL database...')
        self.connection = psycopg2.connect(
            host="localhost",
            database="csv_api_db",
            user="postgres",
            password="2524590"
        )
        self.connection.autocommit = True
        if self.connection:
            print("Database connected succesfully")
        with self.connection.cursor() as cursor:
            cursor.execute("CREATE TABLE IF NOT EXISTS csv_files(file_name varchar NOT NULL PRIMARY KEY, data varchar NOT NULL);")

    def add_file(self, file_name, data):
        with self.connection.cursor() as cursor:
            cursor.execute(f"INSERT INTO csv_files(file_name, data) VALUES('{file_name}', '{data}');")

    def get_file(self, file_name):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT data FROM csv_files WHERE file_name = '{file_name}'")
            return cursor.fetchone()

    def delete_file(self, file_name):
        with self.connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM csv_files WHERE file_name = '{file_name}'")

    def get_all_files(self):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT file_name, data FROM csv_files")
            return cursor.fetchall()
