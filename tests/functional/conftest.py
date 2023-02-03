import asyncio
from redis import asyncio as rasyncio
import json
import aiohttp
import pytest
import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from .settings import settings
from .utils.es_helper import prepare_for_es_insert

from .testdata.data import films_data, persons_data, genres_data


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
    # !!! Обязательно заменить hosts, сейчас для теста
    # client = AsyncElasticsearch(hosts=f'http://localhost:9200')
    client = AsyncElasticsearch(hosts=es_url)
    yield client
    await client.close()


@pytest_asyncio.fixture(scope='session')
async def redis_client():
    redis_url = 'redis://{host}:{port}'.format(
            host=settings.redis_host,
            port=settings.redis_port
        )
    client = await rasyncio.from_url(redis_url, encoding='utf8', decode_responses=True)
    # !!! Обязательно заменить hosts, сейчас для теста
    # client = rasyncio.from_url('redis://localhost:6379', encoding='utf8', decode_responses=True)
    yield client
    await client.close()


@pytest_asyncio.fixture(scope="session")
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


async def create_data(es_client: AsyncElasticsearch, index: str, data: list[dict]):

    els_schema_path = f'/functional/testdata/indexes/{index}.json'
    # Для локального запуска
    # els_schema_path = f'../testdata/indexes/{index}.json'
    if not await es_client.indices.exists(index):
        with open(els_schema_path, 'r') as file:
            schema = json.load(file)
        await es_client.indices.create(index=index, body=schema)
    await es_client.indices.refresh(index=index)
    response = await es_client.bulk(index=index, body=prepare_for_es_insert(data, index), refresh=True)
    if response['errors']:
        raise Exception('Ошибка записи данных в Elasticsearch')


@pytest_asyncio.fixture(scope='session', autouse=True)
async def create_films(es_client):
    await create_data(es_client=es_client, index='movies', data=films_data.data)


# @pytest_asyncio.fixture(scope='session', autouse=True)
# async def create_persons(es_client):
#     await create_data(es_client=es_client, index='persons', data=persons_data.data)


@pytest_asyncio.fixture(scope='session', autouse=True)
async def create_genres(es_client):
    await create_data(es_client=es_client, index='genres', data=genres_data.data)


@pytest_asyncio.fixture
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
