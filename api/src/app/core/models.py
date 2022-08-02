from typing import List, Optional
from uuid import UUID

import orjson
from pydantic import BaseModel, Field


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
    user_id: UUID
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
    user_id: UUID
    product_name: str
    created_at: str


class CreatePayment(BaseOrJSONModel):
    id: UUID
    user_id: UUID
    idempotence_uuid: UUID
    payment_system: str
    products: list[Product]
    cart_id: Optional[UUID]
    description: str


class UpdatePayment(BaseOrJSONModel):
    id: UUID
    payment_status: Optional[str]
    paid: bool = False


class Headers(BaseOrJSONModel):
    x_requers_id: str = Field(..., alias='x-request-id')
    host: str = Field(..., alias='Host')

    class Config:
        allow_population_by_field_name = True
