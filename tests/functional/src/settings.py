import pathlib
from pydantic import BaseSettings

LOCAL_ENV = '.env.dev'
DOCKER_ENV = '.env'


class Base(BaseSettings):
    # Project section
    project_name: str

    # Elastic section
    els_port: int
    els_host: str

    # Redis section
    redis_host: str
    redis_port: int

    class Config:

        env_file = f"{pathlib.Path(__file__).resolve().parent.parent.parent.parent}/{DOCKER_ENV}"
        env_file_encoding = 'utf-8'


settings = Base()
