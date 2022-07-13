from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class PaymentsBase(SQLModel):
    currency: Optional[str]
    value: Optional[float]
    description: Optional[str]
    created_at: Optional[str] = None
    payment_id: Optional[str] = None


class Payments(PaymentsBase, table=True):
    id: int = Field(default=None, primary_key=True)


class PaymentsCreate(PaymentsBase):
    pass
