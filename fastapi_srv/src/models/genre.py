from typing import Optional
from uuid import UUID

from pydantic import Field

from .config_mixin import ConfigMixin


class Genre(ConfigMixin):
    uuid: UUID = Field(alias='id')
    name: str
    description: Optional[str] = ''
