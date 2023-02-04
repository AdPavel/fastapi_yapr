from http import HTTPStatus

import pytest
from utils.request_helper import make_request


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'query': '/genres/640d1ac4-0f5a-465b-a75c-45941d28198b'},
            {'status': HTTPStatus.OK, 'length': 3}
        ),
        (
            {'query': '/genres/640d1ac4-0f5a-465b-a75c-45941d281900'},
            {'status': HTTPStatus.NOT_FOUND, 'length': 1}
        ),
        (
            {'query': '/genres/wrong_id'},
            {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1}
        )
    ]
)
@pytest.mark.asyncio
async def test_genres_detail(session, query_data, expected_answer):
    response = await make_request(session, endpoint=query_data['query'])
    assert response['status'] == expected_answer['status']
    assert len(response['body']) == expected_answer['length']


@pytest.mark.asyncio
async def test_genres_list(session):
    response = await make_request(session, endpoint='/genres/', params={'size': 50, 'page': 1})
    assert response['status'] == HTTPStatus.OK
    assert len(response['body']) == 50
