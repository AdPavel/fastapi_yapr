from functools import lru_cache
from uuid import UUID

from src.db.elastic import get_elastic
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from src.models.film import Film
from src.services.common import Service


class FilmService(Service):

    async def get_films_genre_sort(
        self, page: int, size: int, genre_id: UUID = None, sort_: str = None
    ) -> list[Film] | None:

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
    elastic: AsyncElasticsearch = Depends(get_elastic)
) -> FilmService:
    return FilmService(elastic)
