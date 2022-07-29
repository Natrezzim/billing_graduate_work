from typing import List
from uuid import UUID

import orjson
from pydantic import BaseModel, Field


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class OrjsonMixin(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class ProductWithPrice(OrjsonMixin):
    product_id: UUID
    price_id: UUID


class ValidPayment(OrjsonMixin):
    id: UUID
    user_id: str
    cart: List[ProductWithPrice]
    payment_system: str
    payment_status: str
    paid: bool
    created_at: str
    updated_at: str


class ValidListPayments(OrjsonMixin):
    total: int
    items: List[ValidPayment]


class ValidPrice(OrjsonMixin):
    id: UUID
    value: float
    currency: str
    description: str
    is_active: bool


class ValidProduct(OrjsonMixin):
    id: UUID
    name: str
    description: str
    type: str
    prices: List[ValidPrice] = Field(default_factory=list)
