from http import HTTPStatus
from uuid import UUID

from fastapi import HTTPException
from models.config_models import BaseModel


class Genre(BaseModel):
    uuid: UUID
    name: str
    description: str | None = ''


class BasePerson(BaseModel):
    uuid: UUID
    full_name: str


class Person(BasePerson):
    role: list[str]
    film_ids: list[UUID]


class BaseFilm(BaseModel):
    uuid: UUID
    title: str
    imdb_rating: float | None = 0


class Film(BaseFilm):
    description: str | None = ''
    genre: list[Genre] | None = []
    actors: list[BasePerson] | None = []
    writers: list[BasePerson] | None = []
    directors: list[BasePerson] | None = []


class UnauthorizedError(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=HTTPStatus.UNAUTHORIZED, detail='Bearer Token Error')
