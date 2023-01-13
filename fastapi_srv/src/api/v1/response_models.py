from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel


class Genre(BaseModel):
    uuid: UUID
    name: str


class BasePerson(BaseModel):
    uuid: UUID
    full_name: str


class Person(BasePerson):
    role: str
    film_ids: List[UUID]


class Film(BaseModel):
    uuid: UUID
    title: str
    imdb_rating: Optional[float] = 0
    description: Optional[str] = ''
    genre: Optional[List[Genre]] = []
    actors: Optional[List[BasePerson]] = []
    writers: Optional[List[BasePerson]] = []
    directors: Optional[List[BasePerson]] = []
