import pathlib
from pydantic import BaseSettings


class Base(BaseSettings):
    # Project section
    project_name: str = 'movies'

    # Elastic section
    els_port: int = 9200
    # els_host: str = 'localhost'
    els_host: str = 'els'

    # Redis section
    redis_host: str = 'redis'
    redis_port: int = 6379
    # redis_host: str = 'localhost'
    # redis_db: int

    class Config:

        env_file = f"{pathlib.Path(__file__).resolve().parent.parent.parent.parent}/.env"
        env_file_encoding = 'utf-8'


settings = Base()
