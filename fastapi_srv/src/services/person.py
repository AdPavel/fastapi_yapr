from functools import lru_cache
from uuid import UUID

from db.elastic import get_elastic
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from models.film import Film
from services.common import Service


class PersonService(Service):

    async def get_persons_film(self, person_id: UUID = None) -> list[Film] | None:
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
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(elastic)