import os
import psycopg2
from psycopg2 import sql

class DatabaseConnection:
    def __init__(self):
        self.connection = None

    def connect(self):
        print("Connecting to the database" +os.getenv('DB_HOST'))
        try:
            self.connection = psycopg2.connect(
                dbname=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT')
            )
        except Exception as e:
            print(f"Error connecting to the database: {e}")

    def execute_query(self, query, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

    def execute_update(self, query, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)

    def execute_insert(self, query, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)

    def execute_delete(self, query, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
    def commit(self):
        self.connection.commit()
    def close(self):
        if self.connection:
            self.connection.close()

    def execute_paged_query(self, query, page, page_size, params=None):
        offset = (page - 1) * page_size
        paged_query = f"{query} LIMIT %s OFFSET %s"
        paged_params = params + (page_size, offset) if params else (page_size, offset)
        with self.connection.cursor() as cursor:
            cursor.execute(paged_query, paged_params)
            return cursor.fetchall()