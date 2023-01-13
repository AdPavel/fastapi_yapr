import pathlib
from pydantic import BaseSettings


class Base(BaseSettings):
    # Project section
    project_name: str

    # Elastic section
    els_port: int
    # els_host: str = 'localhost'
    els_host: str

    # Redis section
    redis_host: str
    redis_port: int
    # redis_host: str = 'localhost'
    # redis_db: int

    class Config:

        env_file = f"{pathlib.Path(__file__).resolve().parent.parent.parent.parent}/.env"
        env_file_encoding = 'utf-8'


settings = Base()
