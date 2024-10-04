from sqlalchemy import select
from sqlalchemy.orm import joinedload

from warehous_manager.utils.repository import SQLAlchemyRepository
from warehous_manager.models.orders import Order
from warehous_manager.models.order_items import OrderItem

class OrderRepository(SQLAlchemyRepository):
    model = Order
    '''
    async def get_one(self, data: dict):
        order_id = data['id']
        query = (
                select(Order)
                .options(joinedload(Order.items)
                         .joinedload(OrderItem.product)
                         )
                .where(Order.id == order_id)
            )
        result = await self.session.execute(query)
        return result.unique().scalars().one()
    '''