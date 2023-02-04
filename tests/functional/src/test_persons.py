import json
import uuid

import pytest
from utils.request_helper import make_request
from http import HTTPStatus


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'query': '/persons/640d1ac4-0f5a-465b-a75c-45945d28198b'},
            {'status': HTTPStatus.OK, 'length': 4}
        ),
        (
            {'query': '/persons/641d1ac4-0f5a-465b-a75c-45945d28198b'},
            {'status': HTTPStatus.NOT_FOUND, 'length': 1}
        ),
        (
            {'query': '/persons/wrong_id'},
            {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1}
        )
    ]
)
@pytest.mark.asyncio
async def test_persons_detail(session, query_data, expected_answer):
    response = await make_request(session, endpoint=query_data['query'])
    assert response['status'] == expected_answer['status']
    assert len(response['body']) == expected_answer['length']


@pytest.mark.asyncio
async def test_persons_list(session):
    response = await make_request(session, endpoint='/persons/', params={'size': 50, 'page': 1})
    assert response['status'] == HTTPStatus.OK
    assert len(response['body']) == 50


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'query': '/persons/640d1ac4-0f5a-465b-a75c-45945d28198b/film/'},
            {'status': HTTPStatus.OK, 'length': 1}
        ),
        (
            {'query': '/persons/330d1ac4-0f5a-465b-a75c-45945d28198b/film/'},
            {'status': HTTPStatus.NOT_FOUND, 'length': 1}
        ),
        (
            {'query': '/persons/wrong_id/film/'},
            {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1}
        )
    ]
)
@pytest.mark.asyncio
async def test_persons_films(session, query_data, expected_answer):
    response = await make_request(session, endpoint=query_data['query'])
    assert response['status'] == expected_answer['status']
    assert len(response['body']) == expected_answer['length']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'query': 'Bob'},
            {'status': HTTPStatus.OK, 'length': 50}
        ),
        (
            {'query': 'Mashed potato'},
            {'status': HTTPStatus.NOT_FOUND, 'length': 1}
        )
    ]
)
@pytest.mark.asyncio
async def test_search_person(session, query_data: dict, expected_answer: dict):
    response = await make_request(session, endpoint='/persons/search', params=query_data)
    assert response['status'] == expected_answer['status']
    assert len(response['body']) == expected_answer['length']


@pytest.mark.asyncio
async def test_cache_person(session, es_client, redis_client):

    person_id = uuid.uuid4()
    data = {'id': person_id, 'name': 'Test', 'role': [], 'film_ids': []}
    await es_client.create('persons', person_id, data)

    response_before_delete = await make_request(session, f'/persons/{person_id}/')
    assert response_before_delete['status'] == HTTPStatus.OK

    await es_client.delete('persons', person_id)

    cache_key = f'persons:api.v1.persons:persons_detail:{person_id}'
    redis_data = await redis_client.get(cache_key)

    assert json.loads(redis_data) == response_before_delete['body']

    response_after_delete = await make_request(session, f'/persons/{person_id}/')
    assert response_after_delete['status'] == HTTPStatus.OK
    assert response_before_delete['body'] == response_after_delete['body']
