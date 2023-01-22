from logging import config as logging_config

import uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio

from api.v1 import films, genres, persons
from core.logger import LOGGING
from core.settings import settings
from db import elastic, redis


logging_config.dictConfig(LOGGING)

app = FastAPI(
    title=f"Read-only API для онлайн-кинотеатра: {settings.project_name}",
    description="Информация о фильмах, жанрах и людях, участвовавших в создании произведения",
    version="1.0.0",
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    redis.redis = asyncio.from_url(
        f'redis://{settings.redis_host}:{settings.redis_port}',
        encoding='utf8',
        decode_responses=True
    )
    elastic.es = AsyncElasticsearch(hosts=[f'{settings.els_host}:{settings.els_port}'])
    FastAPICache.init(RedisBackend(redis.redis), prefix="fastapi-cache", expire=60 * 5)


@app.on_event('shutdown')
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()


app.include_router(films.router, prefix='/api/v1/films', tags=['Фильмы'])
app.include_router(genres.router, prefix='/api/v1/genres', tags=['Жанры'])
app.include_router(persons.router, prefix='/api/v1/persons', tags=['Персоны'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8001,
    )
