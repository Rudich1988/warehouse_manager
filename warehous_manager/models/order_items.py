from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, ForeignKey, CheckConstraint, Numeric, String

from warehous_manager.db.db import ModelBase


class OrderItem(ModelBase):
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )
    quantity: Mapped[int] = mapped_column(
        #CheckConstraint('quantity > 0')
    )
    product_price: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2),
        #CheckConstraint('price > 0')
    )
    product_name: Mapped[str] = mapped_column(String(128))
    order_id: Mapped[int] = mapped_column(
        ForeignKey(
            'orders.id',
            ondelete='CASCADE'
        ),
        index=True
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey(
            'products.id'
        ),
        index=True
    )

    order: Mapped['Order'] = relationship(
        'Order',
        back_populates='items'

    )
    product: Mapped['Product'] = relationship(
        'Product',
        back_populates='items'
    )
