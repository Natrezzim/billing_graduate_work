from typing import Optional
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import CreatePayment, UpdatePayment
from app.db.repository.base import BaseRepository
from app.db.models import Cart, Payments, Status, Products


class PaymentRepository(BaseRepository):
    async def create_new_payment(self, payment: CreatePayment):
        async with self.session() as session:
            payment.cart_id = await self._create_cart(session, [item.dict() for item in payment.products])
            p = payment.dict()
            p.pop('products')
            await self._create_payment(session, p)
            await self._create_status(session)
            session.commit()

    async def update_payment(self, payment: UpdatePayment):
        async with self.session() as session:
            await self._create_status(session, payment)

    @staticmethod
    async def _create_cart(session: AsyncSession, products: list[dict]):
        create_products_query = (insert(Products).values(products)
                                 .on_conflict_do_nothing(index_elements=['name', 'value', 'currency'])
                                 .returning(Products))
        create_cart_query = insert(Cart).returning(Cart)
        products = await session.execute(create_products_query)
        cart = await session.execute(create_cart_query)
        for product in products:
            cart.products.append(product)
        return cart.id

    @staticmethod
    async def _create_payment(session: AsyncSession, payment: dict):
        query = insert(Payments).values(payment).returning(Payments.id)
        await session.execute(query)

    @staticmethod
    async def _create_status(session, payment: Optional[UpdatePayment]):
        query = (insert(Status).values(payment_id=payment.id, status=payment.payment_status, paid=payment.paid)
                 if payment else insert(Status).values(payment_id=payment.id))
        await session.execute(query)
