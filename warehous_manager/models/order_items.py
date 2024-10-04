from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, ForeignKey, CheckConstraint

from warehous_manager.db.db import ModelBase


class OrderItem(ModelBase):
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )
    quantity: Mapped[int] = mapped_column(
        CheckConstraint('quantity > 0')
    )
    order_id: Mapped[int] = mapped_column(
        ForeignKey(
            'orders.id',
            ondelete='CASCADE'
        ),
        index=True
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey(
            'products.id',
            ondelete='CASCADE'
        ),
        index=True
    )

    order: Mapped['Order'] = relationship(
        #backref='items',
        'Order',
        back_populates='items',
        #lazy='selectin'
        #foreign_keys=[order_id]

    )
    product: Mapped['Product'] = relationship(
        #backref='items',
        'Product',
        back_populates='items',
        #lazy='selectin'
        #foreign_keys=[product_id]
    )
