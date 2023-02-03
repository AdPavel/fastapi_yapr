from http import HTTPStatus
from uuid import UUID

from api.v1.message import PERSON_MSG
from api.v1.models.response_models import Person, BaseFilm
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_cache.decorator import cache
from services.person import PersonService, get_service

from typing import Optional
from starlette.requests import Request
from starlette.responses import Response

router = APIRouter()


def redis_persons_key_by_id(
        func,
        namespace: Optional[str] = "",
        request: Request = None,
        response: Response = None,
        *args,
        **kwargs,
):
    prefix = 'persons'
    cache_key = f"{prefix}:{func.__module__}:{func.__name__}:{kwargs['kwargs']['person_id']}"
    return cache_key


@router.get(
    '/search',
    response_model=list[Person],
    summary="Поиск персоны",
    description="Поиск персоны",
    response_description="Найденные персоны"
)
@cache()
async def search_person(
        query: str = Query(default=..., title='Что искать'),
        page: int = Query(default=1, ge=1, alias='page[number]', title='Страница'),
        size: int = Query(default=50, ge=1, alias='page[size]', title='Количество персон на странице'),
        person_service: PersonService = Depends(get_service)
) -> list[Person]:
    persons = await person_service.get_all(page=page, size=size, key='persons',
                                           query=query, fields=['name'])
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=PERSON_MSG)

    return [Person(**person.dict()) for person in persons]


@router.get(
    '/',
    response_model=list[Person],
    summary="Список персон",
    description="Список персон",
    response_description="Список персон"
)
@cache()
async def persons_list(
        page: int = Query(default=1, ge=1, alias='page[number]', title='Страница'),
        size: int = Query(default=50, ge=1, alias='page[size]', title='Количество персон на странице'),
        person_service: PersonService = Depends(get_service)
) -> list[Person]:

    persons = await person_service.get_all(page=page, size=size, key='persons')
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=PERSON_MSG)

    return [Person(**person.dict()) for person in persons]


@router.get(
    '/{person_id}/film',
    response_model=list[BaseFilm],
    summary="Фильмы по персоне",
    description="Фильмы по персоне",
    response_description="Фильмы по персоне"
)
@cache()
async def persons_films(
        person_id: UUID,
        person_service: PersonService = Depends(get_service)
) -> list[BaseFilm]:
    films = await person_service.get_persons_film(person_id)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=PERSON_MSG)
    return [BaseFilm(**film.dict()) for film in films]


@router.get(
    '/{person_id}',
    response_model=Person,
    summary="Детализация по персоне",
    description="Подробнее по персоне",
    response_description="Подробнее по персоне"
)
@cache(key_builder=redis_persons_key_by_id)
async def persons_detail(
        person_id: UUID,
        person_service: PersonService = Depends(get_service)
) -> Person:
    person = await person_service.get_by_id(person_id, key='persons')
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=PERSON_MSG)
    return Person(**person.dict())
