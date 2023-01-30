import asyncio
import uuid

import aiohttp
import pytest
import pytest_asyncio
from elasticsearch import AsyncElasticsearch, helpers
from settings import settings
from utils.es_helper import prepare_for_es_insert, prepare_for_es_delete

from testdata.data import films_data

@pytest.fixture(scope="session")
def event_loop():
    """Overrides pytest default function scoped event loop"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def es_client():
    es_url = 'http://{host}:{port}'.format(
        host=settings.els_host,
        port=settings.els_port
    )
    client = AsyncElasticsearch(hosts=es_url)
    yield client
    await client.close()


@pytest_asyncio.fixture(scope="session")
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()
#
# @pytest_asyncio.fixture(scope='session')
# async def create_film(es_client):
#     index = 'movies'
#     data = [
#         {
#             'id': str(uuid.uuid4()),
#             'imdb_rating': 8.5,
#             'genre': [
#                 {'id': str(uuid.uuid4()), 'name': 'Action'},
#                 {'id': str(uuid.uuid4()), 'name': 'Sci-Fi'}
#             ],
#             'title': 'The Star',
#             'description': 'New World',
#             'directors_names': ['Stan', 'Quentin'],
#             'actors_names': ['Ann', 'Bob'],
#             'writers_names': ['Ben', 'Howard'],
#             'directors': [
#                 {'id': str(uuid.uuid4()), 'name': 'Ann'},
#                 {'id': str(uuid.uuid4()), 'name': 'Bob'}
#             ],
#             'actors': [
#                 {'id': str(uuid.uuid4()), 'name': 'Ann'},
#                 {'id': str(uuid.uuid4()), 'name': 'Bob'}
#             ],
#             'writers': [
#                 {'id': str(uuid.uuid4()), 'name': 'Ben'},
#                 {'id': str(uuid.uuid4()), 'name': 'Howard'}
#             ],
#         }
#     ]
#
#     # await helpers.async_bulk(es_client, prepare_for_es_insert(data, index))
#     await es_client.indices.refresh(index=index)
#     # await asyncio.sleep(1)
#
#     yield data
#
#     # await helpers.async_bulk(es_client, prepare_for_es_delete(data, index))


# async def create_data(es_client: AsyncElasticsearch, index: str):
#     # els_schema_path = f'testdata/indexes/{index}.json'
#     #
#     # # if not await es_client.indices.exists(index=index):
#     # #     await es_client.indices.create(index, body=els_schema_path)
#     # # # if not await es_client.indices.exists(index=index):
#     # # #     await es_client.indices.create(index, els_schema_path['body'])
#     # # # bulk_query = []
#     # # # for row in data:
#     # # #     action = {"index": {"_index": index_name, "_id": row["id"]}}
#     # # #     doc = row
#     # # #     bulk_query.append(action)
#     # # #     bulk_query.append(doc)
#     # # await async_bulk(es_client, prepare_for_es_insert(films_data.data, index))
#     # data = prepare_for_es_insert(films_data.data, 'movies')
#     # response = await es_client.bulk(index=index, body=data, refresh=True)
#     # await es_client.close()
#     # if response['errors']:
#     #     raise Exception('Ошибка записи данных в Elasticsearch')
#     # await es_client.indices.refresh(index=index)
#     # await asyncio.sleep(1)


@pytest.fixture
def create_film():
    async def inner(data=films_data.data):
        bulk_query = prepare_for_es_insert(data, 'movies')

        es_client = AsyncElasticsearch(hosts=f'http://{settings.els_host}:{settings.els_port}',
                                       validate_cert=False,
                                       use_ssl=False)
        response = await es_client.bulk(bulk_query, refresh=True)
        await es_client.close()
        if response['errors']:
            raise Exception('Ошибка записи данных в Elasticsearch')

    return inner


@pytest_asyncio.fixture(scope='session')
def make_request(session):
    async def inner(endpoint: str, params: dict = {}) -> dict:

        url = settings.test_service_url + '/api/v1' + endpoint

        async with session.get(url=url, params=params) as response:
            response = {
                'body': await response.json(),
                'headers': response.headers,
                'status': response.status,
            }
            return response

    return inner


