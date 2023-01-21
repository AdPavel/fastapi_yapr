from http import HTTPStatus
from uuid import UUID

from api.v1.models.query_models import Sort
from api.v1.models.response_models import Film, BaseFilm
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_cache.decorator import cache
from services.film import FilmService, get_service

router = APIRouter()


@router.get(
    '/search',
    response_model=list[BaseFilm],
    summary="Поиск фильма",
    description="Поиск фильма",
    response_description="Найденные фильмы"
)
@cache()
async def search_films(
        query: str = Query(default=..., title='Что искать'),
        page: int = Query(default=1, ge=1, alias='page[number]', title='Страница'),
        size: int = Query(default=50, ge=1, alias='page[size]', title='Количество фильмов на странице'),
        film_service: FilmService = Depends(get_service)
) -> list[BaseFilm]:
    films = await film_service.get_all_from_elastic(page=page, size=size, query=query,
                                                    fields=['title', 'description'], key='movies')
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='films not found')

    return [BaseFilm(**film.dict()) for film in films]


@router.get(
    '/{film_id}',
    response_model=Film,
    summary="Детализация по фильму",
    description="Детализированная информация по фильму",
    response_description="Детализированная информация по фильму"
)
@cache()
async def film_details(
        film_id: UUID,
        film_service: FilmService = Depends(get_service)
) -> Film:
    film = await film_service.get_by_id(film_id, key='movies')
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')

    return Film(**film.dict())


@router.get(
    '/',
    response_model=list[BaseFilm],
    summary="Фильмы",
    description="Фильмы",
    response_description="Фильмы"
)
@cache()
async def get_films_by_genre(
        genre: UUID = Query(default=None, alias='filter[genre]', title='Жанр'),
        sort: Sort = Query(default=Sort.imdb_rating_desc, title='Сортировка'),
        page: int = Query(default=1, ge=1, alias='page[number]', title='Страница'),
        size: int = Query(default=50, ge=1, alias='page[size]', title='Количество фильмов на странице'),
        film_service: FilmService = Depends(get_service)
) -> list[BaseFilm]:

    films = await film_service.get_films_genre_sort(page=page, size=size, genre_id=genre, sort_=sort.value)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='films not found')

    return [BaseFilm(**film.dict()) for film in films]

