from decimal import Decimal
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, ForeignKey, Numeric, String

from warehous_manager.db.db import ModelBase


class OrderItem(ModelBase):
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )
    quantity: Mapped[int] = mapped_column()
    product_price: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2)
    )
    product_name: Mapped[str] = mapped_column(String(128))
    order_id: Mapped[int] = mapped_column(
        ForeignKey(
            'orders.id',
            ondelete='CASCADE'
        ),
        nullable=True,
        index=True
    )
    product_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(
            'products.id',
            ondelete='SET NULL'
        ),
        nullable=True,
        index=True
    )

    order: Mapped['Order'] = relationship(
        'Order',
        back_populates='items'

    )
    product: Mapped[Optional['Product']] = relationship(
        'Product',
        back_populates='items'
    )
