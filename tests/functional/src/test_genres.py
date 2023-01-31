import pytest
import uuid


@pytest.mark.asyncio
async def test_genres_detail(make_request):
    response = await make_request(endpoint='/genres/640d1ac4-0f5a-465b-a75c-45941d28198b')
    assert response['status'] == 200
    assert len(response['body']) == 3


@pytest.mark.asyncio
async def test_genres_list(make_request):
    response = await make_request(endpoint='/genres/', params={'size': 50, 'page': 1})
    assert response['status'] == 200
    assert len(response['body']) == 50


@pytest.mark.asyncio
async def test_cache_genre(make_request, es_client):

    genre_id = uuid.uuid4()
    data = {'id': genre_id, 'name': 'Test'}
    await es_client.create('genres', genre_id, data)

    response_before_delete = await make_request(f'/genres/{genre_id}/')
    assert response_before_delete['status'] == 200

    await es_client.delete('genres', genre_id)

    response_after_delete = await make_request(f'/genres/{genre_id}/')
    assert response_after_delete['status'] == 200
    assert response_before_delete['body'] == response_after_delete['body']
