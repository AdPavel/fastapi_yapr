from pydantic import BaseModel
from typing import Optional
from .config_mixin import ConfigMixin


class Genre(BaseModel, ConfigMixin):
    id: str
    name: str
    description: Optional[str] = ''
