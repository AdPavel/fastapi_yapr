from enum import Enum


class Sort(str, Enum):
    imdb_rating_desc = '-imdb_rating'
    imdb_rating_asc = 'imdb_rating'
