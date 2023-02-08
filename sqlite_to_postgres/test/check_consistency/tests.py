import os
import sqlite3
from contextlib import closing
from datetime import datetime

import psycopg2
import pytest
from dotenv import load_dotenv
from psycopg2.extras import DictCursor

from sqlite_to_postgres.load_data import load_from_sqlite


@pytest.fixture()
def load_env():
    load_dotenv()


def test_integrity(load_env):
    """Проверка целостности данных."""

    dsl = {
        'dbname': os.environ.get('DBNAME'),
        'user': os.environ.get('USER'),
        'password': os.environ.get('PASSWORD'),
        'host': os.environ.get('HOST'),
        'port': os.environ.get('PORT')
    }
    db_name = 'db.sqlite'

    with closing(sqlite3.connect(db_name)) as sqlite_conn:
        with closing(psycopg2.connect(**dsl, cursor_factory=DictCursor)) as pg_conn:
            load_from_sqlite(
                sqlite_conn,
                pg_conn,
            )
            tables = ('film_work', 'person', 'genre', 'person_film_work', 'genre_film_work')
            for table in tables:
                curs_sl = sqlite_conn.cursor()
                curs_sl.execute(
                    """SELECT count(*) FROM {0}""".format(table)
                )
                count_rows_sl = curs_sl.fetchall()[0][0]

                curs_pg = pg_conn.cursor()
                curs_pg.execute(
                    """SELECT count(*) FROM content.{0}""".format(table)
                )
                count_rows_pg = curs_pg.fetchall()[0][0]

                assert count_rows_pg == count_rows_sl


def test_data(load_env):
    """Тест проверяет содержимое всех таблиц."""

    dsl = {
        'dbname': os.environ.get('DBNAME'),
        'user': os.environ.get('USER'),
        'password': os.environ.get('PASSWORD'),
        'host': os.environ.get('HOST'),
        'port': os.environ.get('PORT')
    }
    db_name = 'db.sqlite'

    with closing(sqlite3.connect(db_name)) as sqlite_conn:
        with closing(psycopg2.connect(**dsl, cursor_factory=DictCursor)) as pg_conn:
            load_from_sqlite(
                sqlite_conn,
                pg_conn,
            )
            tables = ('film_work',)
            sqlite_conn.row_factory = sqlite3.Row
            curs_sl = sqlite_conn.cursor()
            curs_pg = pg_conn.cursor()

            for table in tables:
                curs_sl.execute(
                    """SELECT count(*) FROM {0}""".format(table)
                )
                count_rows = curs_sl.fetchall()[0][0]
                offset = 0
                size = 500

                while offset < count_rows:
                    curs_sl.execute(
                        """SELECT * FROM {0} LIMIT {1} OFFSET {2}""".format(
                            table,
                            size,
                            offset,
                        )
                    )
                    curs_pg.execute(
                        """SELECT * FROM content.{0} LIMIT {1} OFFSET {2}""".format(
                            table,
                            size,
                            offset,
                        )
                    )
                    query_data_sl = [dict(item) for item in curs_sl.fetchall()]
                    query_data_pg = [dict(item) for item in curs_pg.fetchall()]

                    for index, item in enumerate(query_data_pg):
                        for key, value in item.items():
                            if key == 'created':
                                sl = datetime.strptime(
                                    query_data_sl[index].get('created_at') + ':00',
                                    '%Y-%m-%d %H:%M:%S.%f%z',
                                )
                                assert sl == value
                            elif key == 'modified':
                                sl = datetime.strptime(
                                    query_data_sl[index].get('updated_at') + ':00',
                                    '%Y-%m-%d %H:%M:%S.%f%z',
                                )
                                assert sl == value
                            else:
                                assert query_data_sl[index].get(key) == value

                    offset += size
