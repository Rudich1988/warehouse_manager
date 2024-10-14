from decimal import Decimal
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, ForeignKey, Numeric, String, UniqueConstraint, Index

from warehous_manager.db.db import ModelBase


class OrderItem(ModelBase):
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )
    product_count: Mapped[int] = mapped_column()
    product_price: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2)
    )
    product_name: Mapped[str] = mapped_column(String(128))
    order_id: Mapped[int] = mapped_column(
        ForeignKey(
            'orders.id',
            ondelete='CASCADE'
        ),
        nullable=True
    )
    product_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(
            'products.id',
            ondelete='SET NULL'
        ),
        nullable=True
    )

    order: Mapped['Order'] = relationship(
        'Order',
        back_populates='items'

    )
    product: Mapped[Optional['Product']] = relationship(
        'Product',
        back_populates='items'
    )

    __table_args__ = (
        UniqueConstraint(
            'order_id',
            'product_id',
            name='ix_order_items_order_id_product_id'
        ),
    )
