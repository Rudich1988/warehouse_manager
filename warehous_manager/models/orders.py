from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, String
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

    items = relationship('OrderItem', lazy='selectin')
