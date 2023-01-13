from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel


class Genre(BaseModel):
    uuid: UUID
    name: str


class Person(BaseModel):
    uuid: UUID
    full_name: str
    role: str
    film_ids: List[UUID]


class Film(BaseModel):
    uuid: UUID
    title: str
    imdb_rating: Optional[float] = 0
    description: Optional[str] = ''
    genre: Optional[List[Genre]] = []
    actors: Optional[List[Person]] = []
    writers: Optional[List[Person]] = []
    directors: Optional[List[Person]] = []
