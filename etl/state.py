import abc
from typing import Any

from redis import Redis


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, key: str, value: str) -> None:
        """Сохранить состояние в постоянное хранилище"""
        raise NotImplementedError

    @abc.abstractmethod
    def retrieve_state(self, key: str) -> str:
        """Загрузить состояние локально из постоянного хранилища"""
        raise NotImplementedError


class RedisStorage(BaseStorage):

    def __init__(self, redis_adapter: Redis):
        self.redis_adapter = redis_adapter

    def save_state(self, key: str, value: str) -> None:
        self.redis_adapter.set(name=key, value=value)

    def retrieve_state(self, key: str) -> str:
        return self.redis_adapter.get(key)


class State:
    """
    Класс для хранения состояния при работе с данными, чтобы постоянно не перечитывать данные с начала.
    Здесь представлена реализация с сохранением состояния в файл.
    В целом ничего не мешает поменять это поведение на работу с БД или распределённым хранилищем.
    """

    def __init__(self, storage: BaseStorage):
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа"""

        self.storage.save_state(key, value)

    def get_state(self, key: str) -> Any:
        """Получить состояние по определённому ключу"""

        return self.storage.retrieve_state(key)
