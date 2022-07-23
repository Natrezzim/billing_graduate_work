from pydantic import BaseModel
from typing import List
from uuid import UUID


class Product(BaseModel):
    name: str
    value: float
    currency: str


class AdminPayment(BaseModel):
    id: UUID
    username: str
    cart: List[Product]
    payment_status: str
    payment_system: str
    paid: bool
    created_at: str
    updated_at: str


class AdminPayments(BaseModel):
    total: int
    items: List[AdminPayment]

    def __init__(self, items):
        total = len(items)
        super().__init__(total=total, items=items)
