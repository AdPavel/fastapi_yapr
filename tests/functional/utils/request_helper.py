from settings import settings


async def make_request(session, endpoint: str, params: dict = {}) -> dict:

    url = settings.test_service_url + '/api/v1' + endpoint

    async with session.get(url=url, params=params) as response:
        response = {
            'body': await response.json(),
            'headers': response.headers,
            'status': response.status,
        }
        return response
