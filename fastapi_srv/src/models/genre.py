from uuid import UUID

from pydantic import Field

from .config_models import BaseConfig


class Genre(BaseConfig):
    uuid: UUID = Field(alias='id')
    name: str
    description: str | None = ''
