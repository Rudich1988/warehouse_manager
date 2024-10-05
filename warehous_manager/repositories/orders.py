from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import array_agg
from sqlalchemy.orm import selectinload

from warehous_manager.utils.repository import SQLAlchemyRepository
from warehous_manager.models.orders import Order
from warehous_manager.models.order_items import OrderItem


class OrderRepository(SQLAlchemyRepository):
    model = Order

    async def get_one(self, data: dict):
        query = (
            select(self.model)
            .options(selectinload(self.model.items))
            .where(self.model.id == data['id'])
        )
        '''
        query = (
            select(
                unique(Order),
                func.array_agg(
                    func.json_build_object(
                        'id', OrderItem.id,
                        'product_name', OrderItem.product_name,
                        'product_price', OrderItem.product_price,
                        'quantity', OrderItem.quantity
                    )
                ).label('items')
            )
            .outerjoin(OrderItem, Order.id == OrderItem.order_id)
            .where(Order.id == data['id'])
            .group_by(Order.id)
        )
        '''
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
