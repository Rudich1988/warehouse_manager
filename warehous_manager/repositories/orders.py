from sqlalchemy import select
from sqlalchemy.orm import selectinload

from warehous_manager.utils.repository import SQLAlchemyRepository
from warehous_manager.models.orders import Order


class OrderRepository(SQLAlchemyRepository):
    model = Order

    async def get_one(self, data: dict):
        query = (
            select(self.model)
            .options(selectinload(self.model.items))
            .where(self.model.id == data['id'])
        )
        order = await self.session.execute(query)
        order_data = order.scalar_one()
        return order_data

    async def get_objects(self):
        query = (
            select(self.model)
            .options(selectinload(self.model.items))
        )
        orders = await self.session.execute(query)
        orders_data = orders.scalars().all()
        return orders_data
