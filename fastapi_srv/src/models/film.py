from typing import Optional, List

from pydantic import Field

from .genre import Genre
from .person import Person
from .config_mixin import ConfigMixin


class Film(ConfigMixin):
    uuid: str = Field(alias='id')
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
