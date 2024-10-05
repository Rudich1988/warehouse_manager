from sqlalchemy import select
from sqlalchemy.orm import selectinload

from warehous_manager.utils.repository import SQLAlchemyRepository
from warehous_manager.models.orders import Order


class OrderRepository(SQLAlchemyRepository):
    model = Order

    async def get_one(self, data: dict):
        '''
        query = (
            select(self.model, OrderItem)
            .join(OrderItem, self.model.id == OrderItem.order_id)
            .where(self.model.id == data['id'])
        )
        '''
        query = (
            select(Order)
            .options(selectinload(self.model.items))
            .where(self.model.id == data['id'])
        )

        result = await self.session.execute(query)
        order_data = result.fetchall()
        return order_data
