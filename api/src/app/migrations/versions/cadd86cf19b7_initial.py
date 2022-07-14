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


def upgrade() -> None:
    op.create_table(
        'payments',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4),
        sa.Column('idempotence_uuid', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('amount', sa.JSON, nullable=False),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('payment_system', payment_platforms, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.current_timestamp()),

    )
    op.create_table(
        'status',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4),
        sa.Column('payment_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('payments.id'), nullable=False),
        sa.Column('status', payment_status, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.current_timestamp()),
        sa.Column('paid', sa.Boolean, default=False),
        sa.Column('sync', sa.Boolean, default=False)
    )


def downgrade() -> None:
    op.drop_table('payments')
    op.drop_table('status')
