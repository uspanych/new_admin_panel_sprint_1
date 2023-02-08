import sqlite3
from typing import List
from .tables_classes import Filmwork, GenreFilmwork, Genre, PersonFilmwork, Person


class SqliteLoader:
    """Класс для выгрузки данных из sqlite."""

    def __init__(
            self,
            connection
    ):
        self.conn = connection
        self.tableclasses = {
            "film_work": Filmwork,
            "genre": Genre,
            "person": Person,
            "genre_film_work": GenreFilmwork,
            "person_film_work": PersonFilmwork,
        }

    def query(
            self,
            size,
            table,
    ) -> List:
        """Метод выгрузки данных из БД."""

        self.conn.row_factory = sqlite3.Row
        curs = self.conn.cursor()
        curs.execute(
            f"""SELECT * from {table}"""
        )
        while rows := curs.fetchmany(size):
            dt_model = self.tableclasses.get(table)
            yield [dt_model.from_dict(dict(row), by_alias=True) for row in rows]
