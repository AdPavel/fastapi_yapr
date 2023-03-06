import requests
from api.v1.models.response_models import UnauthorizedError
from core.settings import settings


async def get_user_roles(authorization: str | None) -> dict:

    response = requests.get(
        settings.auth_service_url,
        headers={'authorization': authorization}
    )

    if response.ok:
        return response.json()
    raise UnauthorizedError
