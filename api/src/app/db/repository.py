from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from asyncio import get_event_loop
from uuid import UUID

from app.db.postgres import sessionmaker, engine
from app.db.models import Payments, Status, Cart, Products
from app.core.models import AdminPayment, AuthPayment


class SyncRepository:
    def __init__(self):
        self._session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @property
    def session(self):
        return self._session

    async def get_sync_data(self, sync=False) -> (list[AdminPayment], list[AuthPayment]):
        return await self.get_admin_sync_data(sync), await self.get_auth_sync_data(sync)

    async def get_admin_sync_data(self, sync=False) -> list[AdminPayment]:
        async with self.session() as session:
            query = (
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
            res = await session.execute(query)
            return res

    async def get_auth_sync_data(self, sync=False) -> list[AuthPayment]:
        pass

    async def set_sync_flag(self, data: list[UUID]) -> None:
        async with self.session() as session:
            query = update(Status).where(Status.id in data).values(sync=True)
            await session.execute(query)



if __name__ == '__main__':

    loop = get_event_loop()
    x = SyncRepository()
    d = loop.run_until_complete(x.get_admin_sync_data())
    print(d)