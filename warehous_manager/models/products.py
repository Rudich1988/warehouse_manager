from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    BigInteger,
    String,
    Integer,
    Text,
    Numeric,
    CheckConstraint
)

from warehous_manager.db.db import ModelBase


class Product(ModelBase):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2),
        CheckConstraint('price > 0')
    )
    quantity: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint('quantity >= 0')
    )

    items = relationship('OrderItem')

