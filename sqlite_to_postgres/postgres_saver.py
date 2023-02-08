from dataclasses import asdict, fields

import psycopg2.extras

from .tables_classes import Genre, Filmwork, PersonFilmwork, Person, GenreFilmwork


class PostgresSaver:
    """Класс для загрузки данных в Postgresql."""

    def __init__(
            self,
            connection,
    ):
        self.conn = connection
        self.tableclasses = {
            "film_work": Filmwork,
            "genre": Genre,
            "person": Person,
            "genre_film_work": GenreFilmwork,
            "person_film_work": PersonFilmwork,
        }

    def insert(
            self,
            data: list,
            table: str,
    ):
        """Метод для формирования данных к запросу БД."""

        dt_fields = [f.name for f in fields(self.tableclasses.get(table))]
        values = ','.join(f'%({arg})s' for arg in dt_fields)
        columns = ','.join(dt_fields)

        self._query(
            table,
            data,
            values,
            columns,
        )

    def _query(
            self,
            table: str,
            data: list,
            values: str,
            columns: str,
    ):
        """Метод для запроса к БД."""

        curs = self.conn.cursor()
        psycopg2.extras.execute_batch(
            curs,
            f"""INSERT INTO content.{table} ({columns}) VALUES ({values}) ON CONFLICT (id) DO NOTHING""",
            [asdict(item) for item in data],
        )
