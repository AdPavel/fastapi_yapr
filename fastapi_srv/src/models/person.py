from pydantic import Field

from .config_mixin import ConfigMixin


class Person(ConfigMixin):
    uuid: str = Field(alias='id')
    full_name: str = Field(alias='name')
