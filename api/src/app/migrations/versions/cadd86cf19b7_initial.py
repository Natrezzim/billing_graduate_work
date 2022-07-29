"""initial

Revision ID: cadd86cf19b7
Revises: 
Create Date: 2022-07-14 20:00:03.978774

"""
from uuid import uuid4

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = 'cadd86cf19b7'
down_revision = None
branch_labels = None
depends_on = None

payment_platforms = sa.Enum('yookassa', name='payment_platform_enum')
payment_status = sa.Enum('pending', 'succeeded', 'canceled', 'waiting_for_capture', name='payment_status_enum')
currencies = sa.Enum('RUB', 'USD', name='currencies_enum')


def upgrade() -> None:
    op.create_table(
        'cart',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now()),
    )
    op.create_table(
        'payments',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4),
        sa.Column('cart_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('cart.id'), nullable=False),
        sa.Column('idempotence_uuid', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', UUID(as_uuid=True), nullable=False),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('payment_system', payment_platforms, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now()),
    )
    op.create_table(
        'status',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4),
        sa.Column('payment_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('payments.id'), nullable=False),
        sa.Column('status', payment_status, nullable=True),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now()),
        sa.Column('paid', sa.Boolean, default=False),
        sa.Column('sync', sa.Boolean, default=False)
    )
    op.create_table(
        'products',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4),
        sa.Column('name', sa.VARCHAR(100), nullable=False),
        sa.Column('value', sa.Float(asdecimal=True), nullable=False),
        sa.Column('currency', currencies, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP, nullable=False, server_default=sa.func.now()),
    )
    op.create_table(
        'products_to_cart',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4),
        sa.Column('product_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('products.id'), nullable=False),
        sa.Column('cart_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('cart.id'), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now()),
        sa.UniqueConstraint('product_id', 'cart_id', name='product_cart_uix')
    )


def downgrade() -> None:
    op.drop_table('status')
    op.drop_table('products_to_cart')
    op.drop_table('payments')
    op.drop_table('cart')
    op.drop_table('prices')
    op.drop_table('products')
    op.execute('DROP TYPE payment_platform_enum')
    op.execute('DROP TYPE payment_status_enum')
    op.execute('DROP TYPE currencies_enum')
