"""initial

Revision ID: cadd86cf19b7
Revises: 
Create Date: 2022-07-14 20:00:03.978774

"""
from uuid import uuid4
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'cadd86cf19b7'
down_revision = None
branch_labels = None
depends_on = None

payment_platforms = sa.Enum('yookassa', name='payment_platform_enum')
payment_status = sa.Enum('pending', 'succeeded', 'canceled', 'waiting_for_capture', name='payment_status_enum')
currencies = sa.Enum('RUB', 'USD', name='currencies_enum')


def upgrade() -> None:
    op.create_table(
        'payments',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4),
        sa.Column('cart_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('payments.id'), nullable=False),
        sa.Column('idempotence_uuid', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('payment_system', payment_platforms, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now()),
    )
    op.create_table(
        'status',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4),
        sa.Column('payment_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('payments.id'), nullable=False),
        sa.Column('status', payment_status, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now()),
        sa.Column('paid', sa.Boolean, default=False),
        sa.Column('sync', sa.Boolean, default=False)
    )
    op.create_table(
        'products',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4),
        sa.Column('name', sa.VARCHAR(100), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP, nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP, nullable=False, onupdate=sa.func.now()),
    )
    op.create_table(
        'prices',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4),
        sa.Column('product_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('products.id'), nullable=False),
        sa.Column('value', sa.Float(asdecimal=True), nullable=False),
        sa.Column('currency', currencies, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP, nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP, nullable=False, onupdate=sa.func.now()),
        sa.UniqueConstraint('product_id', 'currency', name='product_currency_uix')
    )
    op.create_table(
        'cart',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4),
        sa.Column('username', sa.VARCHAR(100), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.current_timestamp()),
    )
    op.create_table(
        'products_to_cart',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4),
        sa.Column('product_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('products.id'), nullable=False),
        sa.Column('cart_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('cart.id'), nullable=False),
        sa.Column('username', sa.VARCHAR(100), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.current_timestamp()),
        sa.UniqueConstraint('product_id', 'cart_id', name='product_cart_uix')
    )


def downgrade() -> None:
    op.drop_table('payments')
    op.drop_table('status')
    op.drop_table('products')
    op.drop_table('prices')
    op.drop_table('cart')
    op.drop_table('products_to_cart')

