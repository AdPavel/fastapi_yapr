from functools import lru_cache
from uuid import UUID

from db.elastic import get_elastic
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from models.film import Film
from services.common import Service
from storages.film_storage import ElasiticFilmStorage


class FilmService(Service):

    async def get_films_genre_sort(
        self, page: int, size: int, genre_id: UUID = None, sort_: str = None
    ) -> list[Film] | None:

        data = await self.storage.get_films_genre_sort(page, size, genre_id, sort_)
        return data


@lru_cache()
def get_service(
    elastic: AsyncElasticsearch = Depends(get_elastic)
) -> FilmService:
    storage = ElasiticFilmStorage(elastic)
    return FilmService(storage)
