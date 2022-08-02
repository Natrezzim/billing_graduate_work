from datetime import datetime
from uuid import uuid4

from sqlalchemy import (TIMESTAMP, VARCHAR, Boolean, Column, Float, ForeignKey,
                        Table, Text, UniqueConstraint, func)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.postgres import Base
from app.migrations.versions.cadd86cf19b7_initial import (currencies,
                                                          payment_platforms,
                                                          payment_status)


class Payments(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    cart_id = Column(UUID(as_uuid=True), ForeignKey("cart.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    idempotence_uuid = Column(UUID(as_uuid=True), nullable=False)
    description = Column(Text, nullable=False)
    payment_system = Column(payment_platforms, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now())


class Status(Base):
    __tablename__ = "status"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    payment_id = Column(UUID(as_uuid=True), ForeignKey("payments.id", ondelete="CASCADE"), nullable=False)
    status = Column(payment_status, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.now())
    paid = Column(Boolean, default=False)
    sync = Column(Boolean, default=False)


class Products(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    name = Column(VARCHAR(100), nullable=False)
    price_id = Column(UUID(as_uuid=True), nullable=False)
    value = Column(Float(asdecimal=True), nullable=False)
    currency = Column(currencies, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())


ProductsToCart = Table(
        'products_to_cart',
        Base.metadata,
        Column('id', UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4),
        Column('product_id', UUID(as_uuid=True), ForeignKey('products.id'), nullable=False),
        Column('cart_id', UUID(as_uuid=True), ForeignKey('cart.id'), nullable=False),
        Column('created_at', TIMESTAMP, server_default=func.now()),
        UniqueConstraint('product_id', 'cart_id', name='product_cart_uix')
    )


class Cart(Base):
    __tablename__ = 'cart'

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    products = relationship(Products, secondary=ProductsToCart)
