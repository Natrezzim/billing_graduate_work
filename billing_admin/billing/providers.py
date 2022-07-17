import enum
import uuid

import orjson

stub_1 = {
    'cart_id': uuid.uuid4(),
    'idempotence_uuid': uuid.uuid4(),
    'description': 'Description of current transaction'
}


class ProviderName(enum.Enum):
    yookassa = enum.auto()
    test = enum.auto()


class BillingProvider:

    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name

    def process_request(self, request_body: bytes) -> dict:
        pass

    @classmethod
    def get_provider(cls, provider_name):
        if cls.providers is None:
            cls.providers = {}
            for provider_class in cls.__subclasses__():
                provider = provider_class()
                cls.providers[provider.provider_name] = provider
        return cls.providers.get(provider_name)


class YooKassa(BillingProvider):
    def __init__(self):
        super().__init__(ProviderName.yookassa.name)

    def proccess_request(self, request_body: bytes) -> dict:
        try:
            #  Подготовка словаря в соответствии с моделью для записи в БД
            decoded_body = request_body.decode('utf-8')
            body = orjson.loads(decoded_body)
            body = stub_1
            body['payment_system'] = self.provider_name
        except orjson.JSONDecodeError:
            body = None
        return body


class TestProvider(BillingProvider):
    def __init__(self):
        super().__init__(ProviderName.test.name)

    def proccess_request(self, request_body: bytes) -> dict:
        try:
            #  Подготовка словаря в соответствии с моделью для записи в БД
            decoded_body = request_body.decode('utf-8')
            body = orjson.loads(decoded_body)
            body = stub_1
            body['payment_system'] = self.provider_name
        except orjson.JSONDecodeError:
            body = None
        return body
