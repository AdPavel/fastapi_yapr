from uuid import UUID

from pydantic import Field

from .config_mixin import ConfigMixin


class Person(ConfigMixin):
    uuid: UUID = Field(alias='id')
    full_name: str = Field(alias='name')
