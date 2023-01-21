from functools import lru_cache
from typing import Optional
from uuid import UUID

from aioredis import Redis
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from models.film import Film
from services.common import Service


class PersonService(Service):

    async def get_persons_film(self, person_id: UUID = None) -> Optional[list[Film]]:
        person = await super().get_by_id(_id=person_id, key='persons')
        film_ids = person.film_ids
        body = {'query': {'ids': {'values': film_ids}}}

        try:
            result = await self.elastic.search(index='movies', body=body)
            docs = result['hits']['hits']
        except NotFoundError:
            return None
        ls = [Film(**doc['_source']) for doc in docs]
        return ls


@lru_cache()
def get_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
