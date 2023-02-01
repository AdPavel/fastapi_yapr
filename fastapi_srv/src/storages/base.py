import abc


class BaseFilmStorage(abc.ABC):

    @abc.abstractmethod
    async def get_all(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    async def get_by_id(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    async def get_films_genre_sort(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    async def get_persons_film(self, *args, **kwargs):
        pass
