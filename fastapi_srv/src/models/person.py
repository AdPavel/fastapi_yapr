from uuid import UUID
from typing import Optional, List
from pydantic import Field

from .config_models import BaseConfig


class Person(BaseConfig):
    uuid: UUID = Field(alias='id')
    full_name: str = Field(alias='name')


class ExtendedPerson(Person):
    role: Optional[List[str]] = []
    film_ids: Optional[List[UUID]] = []
