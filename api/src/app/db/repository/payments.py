from uuid import UUID

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import CreatePayment, UpdatePayment
from app.db.models import Cart, Payments, Products, Status
from app.db.repository.base import BaseRepository


class PaymentRepository(BaseRepository):
    async def create_new_payment(self, payment: CreatePayment) -> UUID:
        async with self.session() as session:
            payment.cart_id = await self._create_cart(session, [item.dict() for item in payment.products])
            p = payment.dict()
            p.pop('products')
            payment_id = await self._create_payment(session, p)
            await self._create_status(session, payment_id)
            await session.commit()
            return payment_id

    async def update_payment(self, payment: UpdatePayment) -> None:
        async with self.session() as session:
            await self._create_status(
                session, payment_id=payment.id, payment_status=payment.payment_status, paid=payment.paid
            )
            await session.commit()

    @staticmethod
    async def _create_cart(session: AsyncSession, products: list[dict]) -> UUID:
        create_products_query = (insert(Products).values(products)
                                 .on_conflict_do_nothing(index_elements=['name', 'value', 'currency'])
                                 .returning(Products))
        products = await session.execute(create_products_query)

        cart = Cart()
        for product in products:
            cart.products.append(Products(**product))
        session.add(cart)
        await session.flush()
        return cart.id

    @staticmethod
    async def _create_payment(session: AsyncSession, payment: dict) -> UUID:
        query = insert(Payments).values(payment).returning(Payments.id)
        payment_id = (await session.execute(query, payment)).fetchone()[0]
        await session.flush()
        return payment_id

    @staticmethod
    async def _create_status(session, payment_id: UUID, payment_status: str = None, paid: bool = False) -> None:
        query = insert(Status).values(payment_id=payment_id, status=payment_status, paid=paid)
        await session.execute(query)
        await session.flush()
