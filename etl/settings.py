from pydantic import BaseSettings


class PostgresSettings(BaseSettings):
    dbname: str
    user: str
    password: str
    host: str
    port: int

    class Config:
        fields = {
            'dbname': {
                'env': 'DB_NAME',
            },
            'user': {
                'env': 'DB_USER',
            },
            'password': {
                'env': 'DB_PASSWORD',
            },
            'host': {
                'env': 'DB_HOST',
            },
            'port': {
                'env': 'DB_PORT',
            },
        }


class ELSSettings(BaseSettings):
    els_host: str
    els_port: int


class RedisSettings(BaseSettings):
    redis_host: str
    redis_port: int
    redis_db: int


postgres_configs = PostgresSettings()
els_configs = ELSSettings()
redis_configs = RedisSettings()
