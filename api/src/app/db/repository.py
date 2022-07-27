from sqlalchemy import select, update, func, text
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from asyncio import get_event_loop
from uuid import UUID

from app.db.postgres import sessionmaker, engine
from app.db.models import Payments, Status, Cart, Products, ProductsToCart
from app.core.models import AdminPayment, AuthPayment, Product


class SyncRepository:
    def __init__(self):
        self._session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        self.auth_data = list()
        self.admin_data = list()
        self.statuses_ids = list()
        self.all_data = (self.admin_data, self.auth_data)

    @property
    def session(self):
        return self._session

    async def set_sync_data(self, sync=False):
        async with self.session() as session:
            query = await self.get_query(sync)
            for payment, cart, status in await session.execute(query):
                products = [Product(name=p.name, value=p.value, currency=p.currency) for p in cart.products]
                self.statuses_ids.append(status.id)
                await self.add_admin_item(payment, status, products)
                if status.paid:
                    await self.add_auth_item(payment, status, products)

    async def add_admin_item(self, payment, status, products):
        self.admin_data.append(
            AdminPayment(
                id=payment.id,
                username=payment.username,
                cart=products,
                payment_status=status.status,
                payment_system=payment.payment_system,
                paid=status.paid,
                created_at=str(payment.created_at),
                updated_at=str(status.created_at)
            )
        )

    async def add_auth_item(self, payment, status, products):
        self.auth_data.extend(
            AuthPayment(username=payment.username, product_name=p.name, created_at=str(status.created_at))
            for p in products
        )

    @staticmethod
    async def get_query(sync: bool):
        return (
            select(
                Payments,
                Cart,
                Status,
            ).options(selectinload(Cart.products))
            .distinct(Payments.id)
            .where(Payments.id == Status.payment_id)
            .where(Status.sync == sync)
            .where(Payments.cart_id == Cart.id)
            .order_by(Payments.id, Status.created_at.desc())
        )

    async def set_sync_flag(self) -> None:
        async with self.session() as session:
            query = update(Status).where(Status.id in self.statuses_ids).values(sync=True)
            await session.execute(query)


if __name__ == '__main__':

    loop = get_event_loop()
    x = SyncRepository()
    d = loop.run_until_complete(x.get_sync_data())
    from pprint import pprint
    pprint(d)
    loop.run_until_complete(x.set_sync_flag([p.id for p in d[0]]))