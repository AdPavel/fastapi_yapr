from functools import lru_cache
from typing import Union
from uuid import UUID

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.genre import Genre
from models.film import Film
from models.person import ExtendedPerson as Person

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут
models_dict = {'genres': Genre, 'movies': Film, 'persons': Person}


class Service:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, _id: UUID, key: str) -> Union[None, Genre, Film, Person]:
        value = await self._from_cache(str(id), key)
        if not value:
            value = await self._get_from_elastic(_id, key)
            if not value:
                return None
            await self._put_to_cache(value)
        return value

    async def get_all_from_elastic(
            self, page: int, size: int, key: str,
            fields: list = None, query: str = None) -> Union[None, list[Film], list[Genre], list[Person]]:

        if query:
            body = {
                'query': {
                    'multi_match': {
                        'query': query,
                        'fields': fields,
                        'fuzziness': 'auto',
                        'operator': 'and',
                        'boost': 0.5
                    }
                }
            }
        else:
            body = {'query': {'match_all': {}}}
        from_ = (page - 1) * size

        try:
            result = await self.elastic.search(
                index=key, body=body, size=size, from_=from_
            )
            docs = result['hits']['hits']
        except NotFoundError:
            return None
        return [models_dict[key](**doc['_source']) for doc in docs]

    async def _get_from_elastic(self, _id: UUID, key: str) -> Union[None, Genre, Film, Person]:
        try:
            doc = await self.elastic.get(key, _id)
        except NotFoundError:
            return None
        return models_dict[key](**doc['_source'])

    async def _from_cache(self, _id: str, key: str) -> Union[None, Genre, Film, Person]:
        data = await self.redis.get(_id)
        if not data:
            return None
        value = models_dict[key].parse_raw(data)
        return value

    async def _put_to_cache(self, value: Union[Genre, Film, Person]):
        await self.redis.set(str(value.uuid), value.json(), expire=FILM_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> Service:
    return Service(redis, elastic)

