from uuid import UUID
from typing import Optional
from app.core.models import BaseOrJSONModel


class ProductUserRequest(BaseOrJSONModel):
    id: UUID
    price_id: UUID
    name: str
    value: float
    currency: str


class CreatePaymentUserRequest(BaseOrJSONModel):
    id: UUID
    user_id: UUID
    payment_system: str
    products: list[ProductUserRequest]
    description: str

