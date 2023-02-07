from .tables_classes import Filmwork, GenreFilmwork, Genre, PersonFilmwork, Person
from typing import List, Union
import sqlite3


class SqliteLoader:
    """Класс для выгрузки данных из sqlite."""

    def __init__(
            self,
            connection
    ):
        self.conn = connection

    def query(
            self,
            table: str,
            offset: int,
            size: int = 150,
    ) -> List:
        """Метод реализует запросы к БД."""

        self.conn.row_factory = sqlite3.Row
        curs = self.conn.cursor()
        curs.execute(
            'SELECT * FROM {0} LIMIT {1} OFFSET {2}'.format(
                table,
                size,
                offset,
            )
        )
        query_data = curs.fetchall()
        query_list = []
        for item in query_data:
            item = dict(item)
            if table == 'film_work':
                query_list.append(
                    Filmwork(
                        id=item.get('id'),
                        title=item.get('title'),
                        description=item.get('description'),
                        creation_date=item.get('creation_date'),
                        file_path=item.get('file_path'),
                        rating=item.get('rating'),
                        type=item.get('type'),
                        created=item.get('created_at'),
                        modified=item.get('updated_at'),
                    )
                )
            elif table == 'person':
                query_list.append(
                    Person(
                        id=item.get('id'),
                        full_name=item.get('full_name'),
                        created=item.get('created_at'),
                        modified=item.get('updated_at'),
                    )
                )
            elif table == 'genre':
                query_list.append(
                    Genre(
                        id=item.get('id'),
                        name=item.get('name'),
                        description=item.get('description'),
                        created=item.get('created_at'),
                        modified=item.get('updated_at'),
                    )
                )
            elif table == 'person_film_work':
                query_list.append(
                    PersonFilmwork(
                        id=item.get('id'),
                        film_work_id=item.get('film_work_id'),
                        person_id=item.get('person_id'),
                        role=item.get('role'),
                        created=item.get('created_at'),
                    )
                )
            elif table == 'genre_film_work':
                query_list.append(
                    GenreFilmwork(
                        id=item.get('id'),
                        film_work_id=item.get('film_work_id'),
                        genre_id=item.get('genre_id'),
                        created=item.get('created_at'),
                    )
                )

        return query_list

    def table_size(
            self,
            table,
    ) -> Union[str, int]:
        """Метод возвращает количество строк в переданной таблице."""

        try:
            curs = self.conn.cursor()
            curs.execute("SELECT count(*) FROM {0};".format(table))
            count_rows = curs.fetchall()
            return count_rows[0][0]
        except sqlite3.OperationalError:
            return "no such table: {0}".format(table)
