from typing import List
from uuid import UUID

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseOrJSONModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Product(BaseOrJSONModel):
    name: str
    value: float
    currency: str


class AdminPayment(BaseOrJSONModel):
    id: UUID
    username: str
    cart: List[Product]
    payment_status: str
    payment_system: str
    paid: bool
    created_at: str
    updated_at: str


class Payments(BaseOrJSONModel):
    total: int
    items: List[BaseOrJSONModel]

    def __init__(self, items):
        total = len(items)
        super().__init__(total=total, items=items)


class AuthPayment(BaseOrJSONModel):
    username: str
    product_name: str
    created_at: str
