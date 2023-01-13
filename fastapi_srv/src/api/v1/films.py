from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from services.film import FilmService, get_film_service

from .response_models import Film

router = APIRouter()


@router.get('/{film_id}',
            response_model=Film,
            summary="Детализация по фильму",
            description="Детализированая информация по фильму",
            response_description="Детализированая информация по фильму"
            )
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')

    return Film(uuid=film.id, title=film.title)
