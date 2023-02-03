import pytest
import uuid
import json

@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'query': '/genres/640d1ac4-0f5a-465b-a75c-45941d28198b'},
            {'status': 200, 'length': 3}
        ),
        (
            {'query': '/genres/640d1ac4-0f5a-465b-a75c-45941d281900'},
            {'status': 404, 'length': 1}
        )
    ]
)
@pytest.mark.asyncio
async def test_genres_detail(make_request, query_data, expected_answer):
    response = await make_request(endpoint=query_data['query'])
    assert response['status'] == expected_answer['status']
    assert len(response['body']) == expected_answer['length']


@pytest.mark.asyncio
async def test_genres_list(make_request):
    response = await make_request(endpoint='/genres/', params={'size': 50, 'page': 1})
    assert response['status'] == 200
    assert len(response['body']) == 50


@pytest.mark.asyncio
async def test_cache_genre(make_request, es_client, redis_client):

    genre_id = uuid.uuid4()
    data = {'id': genre_id, 'name': 'Test'}
    await es_client.create('genres', genre_id, data)

    response_before_delete = await make_request(f'/genres/{genre_id}/')
    assert response_before_delete['status'] == 200

    await es_client.delete('genres', genre_id)

    cache_key = f'genres:api.v1.genres:genres_detail:{genre_id}'
    redis_data = await redis_client.get(cache_key)

    response_after_delete = await make_request(f'/genres/{genre_id}/')
    assert json.loads(redis_data) == response_before_delete['body']
    assert response_after_delete['status'] == 200
    assert response_before_delete['body'] == response_after_delete['body']
