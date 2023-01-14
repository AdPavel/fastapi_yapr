from uuid import UUID

from pydantic.schema import Optional, List
from pydantic import BaseModel, validator


class Person(BaseModel):
    id: UUID
    name: str
    role: Optional[List]
    film_ids: Optional[List]

    @validator('role')
    def valid_role(cls, value):
        if value is None:
            return []
        return value

    @validator('film_ids')
    def valid_film_ids(cls, value):
        if value is None:
            return []
        return value


class Movie(BaseModel):
    id: UUID
    imdb_rating: Optional[float]
    genre: Optional[List]
    title: str
    description: Optional[str]
    directors_names: Optional[List]
    actors_names: Optional[List]
    writers_names: Optional[List]
    directors: Optional[List]
    actors: Optional[List]
    writers: Optional[List]

    @validator('description')
    def valid_description(cls, value):
        if value is None:
            return ''
        return value

    @validator('directors_names')
    def valid_directors_names(cls, value):
        if value is None:
            return []
        return value

    @validator('actors_names')
    def valid_actors_names(cls, value):
        if value is None:
            return []
        return value

    @validator('writers_names')
    def valid_writers_names(cls, value):
        if value is None:
            return []
        return value

    @validator('directors')
    def valid_directors(cls, value):
        if value is None:
            return []
        return value

    @validator('actors')
    def valid_actors(cls, value):
        if value is None:
            return []
        return value

    @validator('writers')
    def valid_writers(cls, value):
        if value is None:
            return []
        return value


class Genre(BaseModel):
    id: UUID
    name: str
    description: Optional[str]

    @validator('description')
    def valid_description(cls, value):
        if value is None:
            return ''
        return value


transform_models = {
    'movies': Movie,
    'genres': Genre,
    'persons': Person
}
