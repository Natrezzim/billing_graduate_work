
from typing import Optional

from sqlmodel import Field, SQLModel


class PaymentsBase(SQLModel):
    currency: Optional[str]
    value: Optional[float]
    description: Optional[str]
    created_at: Optional[str] = None
    payment_id: Optional[str] = None
    user_id: Optional[str] = None


class Payments(PaymentsBase, table=True):
    id: int = Field(default=None, primary_key=True)


class PaymentsCreate(PaymentsBase):
    pass


class PaymentStatusBase(SQLModel):
    description: Optional[str]
    status: Optional[str]
    created_at: Optional[str]
    user_id: Optional[str]


class PaymentStatus(PaymentStatusBase, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)


class PaymentStatusCreate(PaymentStatusBase):
    pass
