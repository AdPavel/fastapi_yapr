from typing import Optional, List
from uuid import UUID

from pydantic import Field

from .config_mixin import ConfigMixin
from .genre import Genre
from .person import Person


class Film(ConfigMixin):
    uuid: UUID = Field(alias='id')
    title: str
    description: Optional[str] = ''
    genre: Optional[List[Genre]] = []
    imdb_rating: Optional[float] = 0
    directors: Optional[List[Person]] = []
    writers: Optional[List[Person]] = []
    actors: Optional[List[Person]] = []
    directors_names: Optional[List[str]] = []
    writers_names: Optional[List[str]] = []
    actors_names: Optional[List[str]] = []
