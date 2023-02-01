from functools import lru_cache
from uuid import UUID

from db.elastic import get_elastic
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from models.film import Film
from services.common import Service
from storages.film_storage import ElasiticFilmStorage


class PersonService(Service):

    async def get_persons_film(self, person_id: UUID = None) -> list[Film] | None:

        data = await self.storage.get_persons_film(person_id)
        return data


@lru_cache()
def get_service(
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    storage = ElasiticFilmStorage(elastic)
    return PersonService(storage)
