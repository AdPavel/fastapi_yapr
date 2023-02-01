from functools import lru_cache
from uuid import UUID

from db.elastic import get_elastic
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from models.film import Film
from models.genre import Genre
from models.person import ExtendedPerson as Person
from storages.base import BaseFilmStorage
from storages.film_storage import ElasiticFilmStorage


class Service:
    def __init__(self, storage: BaseFilmStorage):
        self.storage = storage

    async def get_all(
        self, page: int, size: int, key: str, fields: list = None, query: str = None
    ) -> None | list[Film] | list[Genre] | list[Person]:
        data = await self.storage.get_all(page, size, key, fields, query)
        return data

    async def get_by_id(self, _id: UUID, key: str) -> None | Genre | Film | Person:

        data = await self.storage.get_by_id(_id, key)
        return data


@lru_cache()
def get_service(
    elastic: AsyncElasticsearch = Depends(get_elastic)
) -> Service:
    storage = ElasiticFilmStorage(elastic)
    return Service(storage)
