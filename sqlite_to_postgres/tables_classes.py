"""Класс представляет из себя описание модели данных для таблиц из movies_database."""
from dataclasses import dataclass, field, fields
import uuid
from datetime import date, datetime


@dataclass(kw_only=True)
class Filmwork:
    title: str
    type: str
    file_path: str
    description: str
    creation_date: date
    rating: float
    modified: datetime = field(metadata={'alias': 'updated_at'})
    created: datetime = field(metadata={'alias': 'created_at'})
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    @classmethod
    def from_dict(cls, user_dict: dict, by_alias=True):
        if by_alias:
            _fields = fields(cls)
            for _field in _fields:
                alias = _field.metadata.get('alias')
                if alias in user_dict.keys():
                    user_dict[_field.name] = user_dict.pop(alias)

        return cls(**user_dict)


@dataclass(kw_only=True)
class Genre:
    name: str
    created: datetime = field(metadata={'alias': 'created_at'})
    modified: datetime = field(metadata={'alias': 'updated_at'})
    description: str = None
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    @classmethod
    def from_dict(cls, user_dict: dict, by_alias=True):
        if by_alias:
            _fields = fields(cls)
            for _field in _fields:
                alias = _field.metadata.get('alias')
                if alias in user_dict.keys():
                    user_dict[_field.name] = user_dict.pop(alias)

        return cls(**user_dict)


@dataclass(kw_only=True)
class Person:
    full_name: str
    created: datetime = field(metadata={'alias': 'created_at'})
    modified: datetime = field(metadata={'alias': 'updated_at'})
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    @classmethod
    def from_dict(cls, user_dict: dict, by_alias=True):
        if by_alias:
            _fields = fields(cls)
            for _field in _fields:
                alias = _field.metadata.get('alias')
                if alias in user_dict.keys():
                    user_dict[_field.name] = user_dict.pop(alias)

        return cls(**user_dict)


@dataclass(kw_only=True)
class PersonFilmwork:
    role: str
    created: datetime = field(metadata={'alias': 'created_at'})
    person_id: uuid = field(default_factory=uuid.uuid4)
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)

    @classmethod
    def from_dict(cls, user_dict: dict, by_alias=True):
        if by_alias:
            _fields = fields(cls)
            for _field in _fields:
                alias = _field.metadata.get('alias')
                if alias in user_dict.keys():
                    user_dict[_field.name] = user_dict.pop(alias)

        return cls(**user_dict)


@dataclass(kw_only=True)
class GenreFilmwork:
    created: datetime = field(metadata={'alias': 'created_at'})
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    genre_id: uuid.UUID = field(default_factory=uuid.uuid4)
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)

    @classmethod
    def from_dict(cls, user_dict: dict, by_alias=True):
        if by_alias:
            _fields = fields(cls)
            for _field in _fields:
                alias = _field.metadata.get('alias')
                if alias in user_dict.keys():
                    user_dict[_field.name] = user_dict.pop(alias)

        return cls(**user_dict)
