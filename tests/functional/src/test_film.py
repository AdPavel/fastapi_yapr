import pytest


@pytest.mark.asyncio
async def test_get_films(create_film, make_request):
    await create_film()
    response = await make_request(endpoint='/films')
    # , params = {'size': 50, 'page': 1}
    assert response.status == 200
    assert len(response.body) == 1