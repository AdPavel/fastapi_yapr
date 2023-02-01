import pytest


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'query': '/films/647d1ac4-0f5a-465b-a75c-45941d28198b'},
                {'status': 200, 'length': 8}
        ),
        (
                {'query': '/films/647d1ac4-0f5a-465b-a75c-45941d281999'},
                {'status': 404, 'length': 1}
        )
    ]
)
@pytest.mark.asyncio
async def test_get_film_by_id(make_request, query_data, expected_answer):
    response = await make_request(endpoint=query_data['query'])
    assert response['status'] == expected_answer['status']
    assert len(response['body']) == expected_answer['length']


@pytest.mark.asyncio
async def test_get_films(make_request):
    response = await make_request(endpoint='/films/', params={'sort': 'imdb_rating', 'size': 50, 'page': 1})
    assert response['status'] == 200
    assert len(response['body']) == 50


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'query': 'The Star'},
                {'status': 200, 'length': 50}
        ),
        (
                {'query': 'Mashed potato'},
                {'status': 404, 'length': 1}
        )
    ]
)
@pytest.mark.asyncio
async def test_film_search(make_request, query_data: dict, expected_answer: dict):
    response = await make_request(endpoint='/films/search', params=query_data)
    assert response['status'] == expected_answer['status']
    assert len(response['body']) == expected_answer['length']


@pytest.mark.asyncio
async def test_cache_film(make_request, es_client):

    film_id = '647d1ac4-0f5a-465b-a75c-45941d28198b'
    response_before_delete = await make_request(endpoint=f'/films/{film_id}')
    assert response_before_delete['status'] == 200

    await es_client.delete('movies', film_id)

    response_after_delete = await make_request(f'/films/{film_id}/')
    assert response_after_delete['status'] == 200
    assert response_before_delete['body'] == response_after_delete['body']