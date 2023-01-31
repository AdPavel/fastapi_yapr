from uuid import UUID

from elasticsearch import AsyncElasticsearch, NotFoundError
from models.film import Film
from models.genre import Genre
from models.person import ExtendedPerson as Person
from storages.base import BaseFilmStorage

models_dict = {'genres': Genre, 'movies': Film, 'persons': Person}


class ElasiticFilmStorage(BaseFilmStorage):

    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def get_by_id(self, _id: UUID, key: str) -> None | Genre | Film | Person:
        try:
            doc = await self.elastic.get(key, _id)
        except NotFoundError:
            return None
        return models_dict[key](**doc['_source'])

    async def get_all(
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

    async def get_persons_film(self, person_id: UUID = None) -> list[Film] | None:
        person = await self.get_by_id(_id=person_id, key='persons')
        film_ids = person.film_ids
        body = {'query': {'ids': {'values': film_ids}}}

        try:
            result = await self.elastic.search(index='movies', body=body)
            docs = result['hits']['hits']
        except NotFoundError:
            return None
        ls = [Film(**doc['_source']) for doc in docs]
        return ls
