from pydantic import BaseModel
from .config_mixin import ConfigMixin


class Person(BaseModel, ConfigMixin):
    id: str
    name: str
