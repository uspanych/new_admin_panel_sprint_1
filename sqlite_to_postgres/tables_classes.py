"""Класс представляет из себя описание модели данных для таблиц из movies_database."""
from dataclasses import dataclass, field
import uuid
from datetime import date, datetime


@dataclass
class Filmwork:
    title: str
    type: str
    modified: datetime
    created: datetime
    file_path: str = None
    description: str = None
    creation_date: date = None
    rating: float = field(default=0.0)
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class Genre:
    name: str
    created: datetime
    modified: datetime
    description: str = None
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class Person:
    full_name: str
    created: datetime
    modified: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class PersonFilmwork:
    role: str
    created: datetime
    person_id: uuid = field(default_factory=uuid.uuid4)
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class GenreFilmwork:
    created: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    genre_id: uuid.UUID = field(default_factory=uuid.uuid4)
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)
