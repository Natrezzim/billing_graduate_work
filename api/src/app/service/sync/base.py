from abc import ABCMeta, abstractmethod
from uuid import uuid4

import orjson
from requests import post

from app.core.models import Headers


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
        headers = Headers(x_requers_id=uuid4().__str__(), host='localhost').dict(by_alias=True)
        result = post(url=self.url, json=orjson.dumps(data), auth=self.auth, headers=headers)
        try:
            res = result.json()
        except:
            res = {}
        return result.status_code, res
