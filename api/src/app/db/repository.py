from fastapi import Depends

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from asyncio import get_event_loop

from app.db.postgres import sessionmaker, engine
from app.db.models import Payments, Status, Cart, Products, Prices, ProductsToCart


class SyncRepository:
    def __init__(self, session):
        self._session = session

    @property
    def session(self):
        return self._session

    async def get_admin_sync_data(self, sync=False):

        async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        async with async_session() as session:
            qwery = (
                select(
                    Payments,
                    Cart,
                    Status,
                    func.max(Status.created_at).label('updated_at')
                ).where(Payments.id == Status.payment_id)
                .where(Status.sync == sync)
                .where(Payments.cart_id == Cart.id)
                .group_by(Status.id, Status.payment_id, Status.status, Status.paid, Status.sync, Payments.id,
                          Cart.id)
            )
            res = await session.execute(qwery)
            return res


if __name__ == '__main__':

    loop = get_event_loop()
    x = SyncRepository(None)
    d = loop.run_until_complete(x.get_admin_sync_data())
    print(d)