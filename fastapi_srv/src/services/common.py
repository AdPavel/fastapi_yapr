from functools import lru_cache
from uuid import UUID

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from models.genre import Genre
from models.film import Film
from models.person import ExtendedPerson as Person


models_dict = {'genres': Genre, 'movies': Film, 'persons': Person}


class Service:
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def get_all_from_elastic(
        self, page: int, size: int, key: str, fields: list = None, query: str = None
    ) -> None | list[Film] | list[Genre] | list[Person]:

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

    async def get_by_id(self, _id: UUID, key: str) -> None | Genre | Film | Person:
        try:
            doc = await self.elastic.get(key, _id)
        except NotFoundError:
            return None
        return models_dict[key](**doc['_source'])


@lru_cache()
def get_service(
    elastic: AsyncElasticsearch = Depends(get_elastic)
) -> Service:
    return Service(elastic)
