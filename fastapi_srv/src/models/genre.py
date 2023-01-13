from typing import Optional

from pydantic import Field

from .config_mixin import ConfigMixin


class Genre(ConfigMixin):
    uuid: str = Field(alias='id')
    name: str
    description: Optional[str] = ''
