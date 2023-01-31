import pytest


@pytest.mark.asyncio
async def test_get_film_by_id(make_request):
    response = await make_request(endpoint='/films/647d1ac4-0f5a-465b-a75c-45941d28198b')
    assert response['status'] == 200
    assert len(response['body']) == 8


@pytest.mark.asyncio
async def test_get_films(make_request):
    response = await make_request(endpoint='/films/', params={'sort': 'imdb_rating', 'size': 50, 'page': 1})
    assert response['status'] == 200
    assert len(response['body']) == 50
