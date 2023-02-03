import json
import uuid

import pytest


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'query': '/persons/640d1ac4-0f5a-465b-a75c-45945d28198b'},
            {'status': 200, 'length': 4}
        ),
        (
            {'query': '/persons/641d1ac4-0f5a-465b-a75c-45945d28198b'},
            {'status': 404, 'length': 1}
        )
    ]
)
@pytest.mark.asyncio
async def test_persons_detail(make_request, query_data, expected_answer):
    response = await make_request(endpoint=query_data['query'])
    assert response['status'] == expected_answer['status']
    assert len(response['body']) == expected_answer['length']


@pytest.mark.asyncio
async def test_persons_list(make_request):
    response = await make_request(endpoint='/persons/', params={'size': 50, 'page': 1})
    assert response['status'] == 200
    assert len(response['body']) == 50


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'query': '/persons/640d1ac4-0f5a-465b-a75c-45945d28198b/film/'},
            {'status': 200, 'length': 1}
        ),
        (
            {'query': '/persons/330d1ac4-0f5a-465b-a75c-45945d28198b/film/'},
            {'status': 404, 'length': 1}
        )
    ]
)
@pytest.mark.asyncio
async def test_persons_films(make_request, query_data, expected_answer):
    response = await make_request(endpoint=query_data['query'])
    assert response['status'] == expected_answer['status']
    assert len(response['body']) == expected_answer['length']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'query': 'Bob'},
                {'status': 200, 'length': 50}
        ),
        (
                {'query': 'Mashed potato'},
                {'status': 404, 'length': 1}
        )
    ]
)
@pytest.mark.asyncio
async def test_search_person(make_request, query_data: dict, expected_answer: dict):
    response = await make_request(endpoint='/persons/search', params=query_data)
    assert response['status'] == expected_answer['status']
    assert len(response['body']) == expected_answer['length']


@pytest.mark.asyncio
async def test_cache_person(make_request, es_client, redis_client):

    person_id = uuid.uuid4()
    data = {'id': person_id, 'name': 'Test', 'role': [], 'film_ids': []}
    await es_client.create('persons', person_id, data)

    response_before_delete = await make_request(f'/persons/{person_id}/')
    assert response_before_delete['status'] == 200

    await es_client.delete('persons', person_id)

    cache_key = f'persons:api.v1.persons:persons_detail:{person_id}'
    redis_data = await redis_client.get(cache_key)

    assert json.loads(redis_data) == response_before_delete['body']

    response_after_delete = await make_request(f'/persons/{person_id}/')
    assert response_after_delete['status'] == 200
    assert response_before_delete['body'] == response_after_delete['body']
