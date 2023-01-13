from typing import Optional, List
from .config_mixin import ConfigMixin


class Film(ConfigMixin):
    id: str
    title: str
    description: Optional[str] = ''
    genre: Optional[List[str]] = []
    imdb_rating: Optional[float] = 0
    directors: Optional[List[dict]] = []
    writers: Optional[List[dict]] = []
    actors: Optional[List[dict]] = []
    directors_names: Optional[List[str]] = []
    writers_names: Optional[List[str]] = []
    actors_names: Optional[List[str]] = []
