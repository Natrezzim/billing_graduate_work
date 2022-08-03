from uuid import UUID
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import CreatePayment, UpdatePayment, Product
from app.db.models import Cart, Payments, Products, Status
from app.db.repository.base import BaseRepository


class PaymentRepository(BaseRepository):
    async def create_new_payment(self, payment: CreatePayment) -> UUID:
        async with self.session() as session:
            payment.cart_id = await self._create_cart(session, payment.products)
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

    async def _create_cart(self, session: AsyncSession, products: list[Product]) -> UUID:
        cart = Cart()
        for product in products:
            product = await self.get_or_create(
                session, Products, name=product.name, value=product.value, currency=product.currency, id=product.id
            )
            cart.products.append(product)
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

    @staticmethod
    async def get_or_create(session, model, id=None, **kwargs):
        query = select(model).filter_by(**kwargs)
        instance = (await session.execute(query)).first()
        if instance:
            return instance[0]
        else:
            instance = model(id=id, **kwargs)
            session.add(instance)
            session.flush()
            return instance
