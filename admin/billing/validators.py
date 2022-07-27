from pydantic import BaseModel
from typing import List
from uuid import UUID


class ValidProduct(BaseModel):
    name: str
    value: float
    currency: str


class ValidPayment(BaseModel):
    id: UUID
    username: str
    cart: List[ValidProduct]
    payment_system: str
    payment_status: str
    paid: bool
    created_at: str
    updated_at: str


class ValidListPayments(BaseModel):
    total: int
    items: List[ValidPayment]
