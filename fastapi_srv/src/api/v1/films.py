from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from services.film import FilmService, get_film_service

from .response_models import Film, BaseFilm

router = APIRouter()


@router.get(
    '/{film_id}',
    response_model=Film,
    summary="Детализация по фильму",
    description="Детализированная информация по фильму",
    response_description="Детализированная информация по фильму"
)
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> Film:
    film = await film_service.get_by_id(film_id)
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
async def get_films(
        page: int = Query(default=1, ge=1, title='Страница'),
        size: int = Query(default=50, ge=1, title='Количество фильмов на странице'),
        film_service: FilmService = Depends(get_film_service)
) -> list[Film]:

    films = await film_service.get_films_from_elastic(page, size)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='films not found')

    return [BaseFilm(**film.dict()) for film in films]
