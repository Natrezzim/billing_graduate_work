from abc import ABCMeta, abstractmethod
from requests import post


class Synchronizer(metaclass=ABCMeta):
    url: str
    auth: str

    @abstractmethod
    async def send_data(self, data: list[dict]) -> (int, dict):
        """
        Метод для отправки данных во внешние сервисы.
        :param data: список оз обхектов для синхронизации.
        :return: (статус ответа, тело ответа)
        """


class BaseSynchronizer(Synchronizer):
    async def send_data(self, data: list[dict]) -> (int, dict):
        result = post(url=self.url, data=data, auth=self.auth)
        return result.status_code, result.json()