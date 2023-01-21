from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from uuid import UUID

from services.person import PersonService, get_service
from api.v1.models.response_models import Person, Film, BaseFilm

router = APIRouter()


@router.get(
    '/search',
    response_model=list[Person],
    summary="Поиск персоны",
    description="Поиск персоны",
    response_description="Найденные персоны"
)
async def search_person(
        query: str = Query(default=..., title='Что искать'),
        page: int = Query(default=1, ge=1, alias='page[number]', title='Страница'),
        size: int = Query(default=50, ge=1, alias='page[size]', title='Количество персон на странице'),
        person_service: PersonService = Depends(get_service)
) -> list[Person]:
    persons = await person_service.get_all_from_elastic(page=page, size=size, key='persons',
                                                        query=query, fields=['name'])
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='persons not found')

    return [Person(**person.dict()) for person in persons]


@router.get('/',
            response_model=list[Person],
            summary="Список персон",
            description="Список персон",
            response_description="Список персон"
            )
async def persons_list(
        page: int = Query(default=1, ge=1, alias='page[number]', title='Страница'),
        size: int = Query(default=50, ge=1, alias='page[size]', title='Количество персон на странице'),
        person_service: PersonService = Depends(get_service)
) -> list[Person]:

    persons = await person_service.get_all_from_elastic(page=page, size=size, key='persons')
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='persons not found')

    return [Person(**person.dict()) for person in persons]


@router.get('/{person_id}/film',
            response_model=list[BaseFilm],
            summary="Фильмы по персоне",
            description="Фильмы по персоне",
            response_description="Фильмы по персоне"
            )
async def persons_films(
        person_id: UUID,
        person_service: PersonService = Depends(get_service)
) -> list[BaseFilm]:
    films = await person_service.get_persons_film(person_id)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return [BaseFilm(**film.dict()) for film in films]


@router.get('/{person_id}',
            response_model=Person,
            summary="Детализация по персоне",
            description="Подробнее по персоне",
            response_description="Подробнее по персоне"
            )
async def persons_detail(
        person_id: UUID,
        person_service: PersonService = Depends(get_service)
) -> Person:
    person = await person_service.get_by_id(person_id, key='persons')
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return Person(**person.dict())
