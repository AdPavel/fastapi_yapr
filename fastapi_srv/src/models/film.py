from uuid import UUID
from pydantic import Field

from .config_models import BaseConfig
from .genre import Genre
from .person import Person


class Film(BaseConfig):
    uuid: UUID = Field(alias='id')
    title: str
    description: str | None = ''
    genre: list[Genre] | None = []
    imdb_rating: float | None = 0
    directors: list[Person] | None = []
    writers: list[Person] | None = []
    actors: list[Person] | None = []
    directors_names: list[str] | None = []
    writers_names: list[str] | None = []
    actors_names: list[str] | None = []
