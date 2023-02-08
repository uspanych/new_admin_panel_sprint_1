import os
import sqlite3
from contextlib import closing

import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from sqlite_to_postgres.postgres_saver import PostgresSaver
from sqlite_to_postgres.sqlite_loader import SqliteLoader


def load_from_sqlite(
        connection: sqlite3.Connection,
        pg_conn: _connection,
     ):
    """Основной метод загрузки данных из SQLite в Postgres"""

    sqlite_loader = SqliteLoader(connection)
    postgres_saver = PostgresSaver(pg_conn)
    tables = ('film_work', 'person', 'genre', 'person_film_work', 'genre_film_work')

    for table in tables:
        size = 200
        for data in sqlite_loader.query(size, table):
            postgres_saver.insert(data, table)

    pg_conn.commit()


if __name__ == '__main__':
    load_dotenv()
    dsl = {
        'dbname': os.environ.get('DBNAME'),
        'user': os.environ.get('USER'),
        'password': os.environ.get('PASSWORD'),
        'host': os.environ.get('HOST'),
        'port': os.environ.get('PORT')
    }

    with closing(sqlite3.connect(os.environ.get('DB_PATH'))) as sqlite_conn:
        with closing(psycopg2.connect(**dsl, cursor_factory=DictCursor)) as pg_conn:
            load_from_sqlite(
                sqlite_conn,
                pg_conn,
            )
