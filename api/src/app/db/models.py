from uuid import uuid4
from datetime import datetime

from sqlalchemy import UniqueConstraint, Column, TIMESTAMP, VARCHAR, ForeignKey, Text, Boolean, Float, func
from sqlalchemy.dialects.postgresql import UUID

from app.db.postgres import Base
from app.migrations.versions.cadd86cf19b7_initial import payment_platforms, payment_status, currencies


class Payments(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    cart_id = Column(UUID(as_uuid=True), ForeignKey("cart.id", ondelete="CASCADE"), nullable=False)
    username = Column(VARCHAR(100), nullable=False)
    idempotence_uuid = Column(UUID(as_uuid=True), nullable=False)
    description = Column(Text, nullable=False)
    payment_system = Column(payment_platforms, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now())


class Status(Base):
    __tablename__ = "status"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    payment_id = Column(UUID(as_uuid=True), ForeignKey("payments.id", ondelete="CASCADE"), nullable=False)
    status = Column(payment_status, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now())
    paid = Column(Boolean, default=False)
    sync = Column(Boolean, default=False)


class Products(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    name = Column(VARCHAR(100), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, onupdate=func.now())


class Prices(Base):
    __tablename__ = 'prices'
    __table_args__ = (UniqueConstraint('product_id', 'currency', name='product_currency_uix'),)

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'), nullable=False)
    value = Column(Float(asdecimal=True), nullable=False)
    currency = Column(currencies, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, onupdate=func.now())


class Cart(Base):
    __tablename__ = 'cart'

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())


class ProductsToCart(Base):
    __tablename__ = 'products_to_cart'
    __table_args__ = (UniqueConstraint('product_id', 'cart_id', name='product_cart_uix'),)

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4),
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'), nullable=False),
    cart_id = Column(UUID(as_uuid=True), ForeignKey('cart.id'), nullable=False),
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
