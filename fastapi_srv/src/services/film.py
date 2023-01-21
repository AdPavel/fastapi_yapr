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

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class FilmService(Service):

    async def get_films_genre_sort(
            self, page: int, size: int, genre_id: UUID = None, sort_: str = None) -> Optional[list[Film]]:

        if genre_id:
            body = {'query': {'nested': {'path': 'genre', 'query': {'match': {'genre.id': genre_id}}}}}
        else:
            body = {'query': {'match_all': {}}}

        from_ = (page - 1) * size
        sort = (f'{sort_[1:]}:desc' if sort_.startswith('-') else f'{sort_}:asc') if sort_ else None

        try:
            result = await self.elastic.search(
                index='movies', body=body, size=size, from_=from_, sort=sort
            )
            docs = result['hits']['hits']
        except NotFoundError:
            return None
        return [Film(**doc['_source']) for doc in docs]


@lru_cache()
def get_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
