import psycopg2.extras
from dataclasses import asdict


class PostgresSaver:
    """Класс для загрузки данных в Postgresql."""

    def __init__(
            self,
            connection,
    ):
        self.conn = connection

    def insert(
            self,
            data: list,
            table: str

    ):
        if table == 'film_work':
            self._insert_to_film_work(data)
        elif table == 'genre':
            self._insert_to_genre(data)
        elif table == 'person':
            self._insert_to_person(data)
        elif table == 'person_film_work':
            self._insert_to_person_film_work(data)
        elif table == 'genre_film_work':
            self._insert_to_genre_film_work(data)

    def _insert_to_film_work(
            self,
            data: list
    ):
        """Метод записывает данные в таблицу film_work."""
        curs = self.conn.cursor()
        psycopg2.extras.execute_batch(
            curs,
            """INSERT INTO content.film_work (title, type, modified, created, file_path, description, creation_date, 
            rating, id) VALUES (%(title)s, %(type)s, %(modified)s, %(created)s, %(file_path)s, %(description)s, 
            %(creation_date)s, %(rating)s, %(id)s) ON CONFLICT (id) DO NOTHING""",
            [asdict(item) for item in data],
        )

    def _insert_to_genre(
            self,
            data: list
    ):
        """Метод записывает данные в таблицу genre."""

        curs = self.conn.cursor()
        psycopg2.extras.execute_batch(
            curs,
            """INSERT INTO content.genre (name, created, modified, description, id)
            VALUES (%(name)s, %(created)s, %(modified)s, %(description)s, %(id)s) 
            ON CONFLICT (id) DO NOTHING""",
            [asdict(item) for item in data],
        )

    def _insert_to_person(
            self,
            data: list
    ):
        """Метод записывает данные в таблицу person."""

        curs = self.conn.cursor()
        psycopg2.extras.execute_batch(
            curs,
            """INSERT INTO content.person (full_name, created, modified, id)
            VALUES (%(full_name)s, %(created)s, %(modified)s, %(id)s) ON CONFLICT (id) DO NOTHING""",
            [asdict(item) for item in data],
        )

    def _insert_to_person_film_work(
            self,
            data: list
    ):
        """Метод записывает данные в таблицу film_work."""

        curs = self.conn.cursor()

        psycopg2.extras.execute_batch(
            curs,
            """INSERT INTO content.person_film_work (role, created, person_id, id, film_work_id)
            VALUES (%(role)s, %(created)s, %(person_id)s, %(id)s, %(film_work_id)s) ON CONFLICT (id) DO NOTHING""",
            [asdict(item) for item in data],
        )

    def _insert_to_genre_film_work(
            self,
            data: list
    ):
        """Метод записывает данные в таблицу genre_film_work."""

        curs: object = self.conn.cursor()
        psycopg2.extras.execute_batch(
            curs,
            """INSERT INTO content.genre_film_work (created, id, genre_id, film_work_id)
            VALUES (%(created)s, %(id)s, %(genre_id)s, %(film_work_id)s) ON CONFLICT (id) DO NOTHING""",
            [asdict(item) for item in data],
        )

    def select(self, table):

        curs = self.conn.cursor()
        curs.execute(
            """SELECT * FROM content.{0}""".format(table)
        )
        data = curs.fetchall()
        return data

    def select_table_size(self, table):

        curs = self.conn.cursor()
        curs.execute(
            """SELECT count(*) FROM content.{0}""".format(table)
        )
        data = curs.fetchall()[0][0]
        return data
