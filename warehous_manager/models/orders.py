from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, String, Integer, Numeric, CheckConstraint
from sqlalchemy.sql import func

from warehous_manager.db.db import ModelBase


class Order(ModelBase):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now()
    )
    status: Mapped[str] = mapped_column(String(128))
    order_cost: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2),
        CheckConstraint('order_cost >= 0'),
        default=Decimal('0.00')
    )
    product_count: Mapped[int] = mapped_column(Integer)

    items = relationship('OrderItem')
