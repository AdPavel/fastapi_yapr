from http import HTTPStatus
from uuid import UUID

from api.v1.models.response_models import Genre
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_cache.decorator import cache
from services.common import Service, get_service
from api.v1.message import GENRES_MSG

router = APIRouter()


@router.get(
    '/',
    response_model=list[Genre],
    summary="Список жанров",
    description="Список жанров",
    response_description="Список жанров"
)
@cache()
async def genres_list(
        page: int = Query(default=1, ge=1, alias='page[number]', title='Страница'),
        size: int = Query(default=50, ge=1, alias='page[size]', title='Количество жанров на странице'),
        genre_service: Service = Depends(get_service)
) -> list[Genre]:

    genres = await genre_service.get_all_from_elastic(page=page, size=size, key='genres')
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=GENRES_MSG)

    return [Genre(**genre.dict()) for genre in genres]


@router.get(
    '/{genre_id}',
    response_model=Genre,
    summary="Детализация по жанру",
    description="Подробнее по жанру",
    response_description="Подробнее по жанру"
)
@cache()
async def genres_detail(genre_id: UUID, genre_service: Service = Depends(get_service)) -> Genre:
    genre = await genre_service.get_by_id(genre_id, key='genres')
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=GENRES_MSG)
    return Genre(**genre.dict())
