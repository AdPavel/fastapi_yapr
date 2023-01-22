from uuid import UUID
from pydantic import Field

from .config_models import BaseConfig


class Person(BaseConfig):
    uuid: UUID = Field(alias='id')
    full_name: str = Field(alias='name')


class ExtendedPerson(Person):
    role: list[str] | None = []
    film_ids: list[UUID] | None = []
