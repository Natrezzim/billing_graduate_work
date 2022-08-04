import uuid
from typing import List, Optional
from uuid import UUID, uuid4

import orjson
from pydantic import BaseModel, Field


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseOrJSONModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class SyncProduct(BaseOrJSONModel):
    product_id: UUID
    price_id: UUID
    product_name: str


class Product(BaseOrJSONModel):
    id: UUID
    price_id: UUID
    name: str
    value: float
    currency: str


class AdminPayment(BaseOrJSONModel):
    id: UUID
    user_id: UUID
    cart: List[SyncProduct]
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
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID = None
    idempotence_uuid: UUID
    payment_system: str
    products: list[Product]
    cart_id: Optional[UUID]
    description: str


class UpdatePayment(BaseOrJSONModel):
    id: UUID
    payment_status: str
    paid: bool = False


class Headers(BaseOrJSONModel):
    x_requers_id: str = Field(..., alias='X-Request-Id')
    host: str = Field(..., alias='Host')
    content_type: str = Field(..., alias='Content-Type')

    class Config:
        allow_population_by_field_name = True
