import pathlib
from pydantic import BaseSettings


class ConfigMix(BaseSettings):
    class Config:
        env_file = f"{pathlib.Path(__file__).resolve().parent.parent}/.env"


class PostgresSettings(ConfigMix, BaseSettings):
    dbname: str
    user: str
    password: str
    host: str
    port: int

    class Config:
        fields = {
            'dbname': {
                'env': 'POSTGRES_DB',
            },
            'user': {
                'env': 'POSTGRES_USER',
            },
            'password': {
                'env': 'POSTGRES_PASSWORD',
            },
            'host': {
                'env': 'POSTGRES_HOST',
            },
            'port': {
                'env': 'POSTGRES_PORT',
            },
        }


class ELSSettings(ConfigMix, BaseSettings):
    els_host: str
    els_port: int


class RedisSettings(ConfigMix, BaseSettings):
    redis_host: str
    redis_port: int
    redis_db: int


postgres_configs = PostgresSettings()
els_configs = ELSSettings()
redis_configs = RedisSettings()
