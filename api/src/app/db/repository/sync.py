from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from app.core.models import AdminPayment, AuthPayment, SyncProduct
from app.db.models import Cart, Payments, Status
from app.db.repository.base import BaseRepository


class SyncRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.admin_data = list()
        self.auth_data = list()
        self.statuses_ids = list()
        self.all_data = (self.admin_data, self.auth_data)

    async def set_sync_data(self, sync=False):
        async with self.session() as session:
            query = await self.get_query(sync)
            for payment, cart, status in await session.execute(query):
                if status.status:
                    products = [SyncProduct(product_id=p.id, price_id=p.price_id, product_name=p.name)
                                for p in cart.products]
                    self.statuses_ids.append(status.id)
                    await self.add_admin_item(payment, status, products)
                    if status.paid:
                        await self.add_auth_item(payment, status, products)

    async def set_sync_flag(self) -> None:
        async with self.session() as session:
            query = update(Status).filter(Status.id.in_(self.statuses_ids)).values(sync=True)
            await session.execute(query)
            await session.commit()

    async def add_admin_item(self, payment, status, products):
        self.admin_data.append(
            AdminPayment(
                id=payment.id,
                user_id=payment.user_id,
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
            AuthPayment(user_id=payment.user_id, product_name=p.product_name, created_at=str(status.created_at))
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
