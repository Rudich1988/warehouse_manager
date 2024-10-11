from sqlalchemy import select
from sqlalchemy.orm import selectinload

from warehous_manager.dto.order_items import OrderItemsDTO
from warehous_manager.utils.repository import SQLAlchemyRepository
from warehous_manager.models.orders import Order
from warehous_manager.dto.orders import OrderResponseDTO


class OrderRepository(SQLAlchemyRepository):
    model = Order

    def create_order_dto(self, order_data):
        items = order_data.items
        order_items = [
            OrderItemsDTO(
                product_count=item.product_count,
                product_name=item.product_name,
                product_price=item.product_price
            ) for item in items
        ]
        order = OrderResponseDTO(
            id=order_data.id,
            created_at=order_data.created_at,
            items=order_items,
            product_count=order_data.product_count,
            status=order_data.status,
            order_cost=order_data.order_cost
        )
        return order

    async def add_one(self, data: dict) -> id:
        order = self.model(**data)
        self.session.add(order)
        await self.session.flush()
        return order.id

    async def get_one(
            self,
            order_id: int
    ) -> OrderResponseDTO:
        query = (
            select(self.model)
            .options(selectinload(self.model.items))
            .where(self.model.id == order_id)
        )
        order = await self.session.execute(query)
        order_data = order.scalar_one()
        return self.create_order_dto(order_data)

    async def get_objects(self) -> list:
        query = (
            select(self.model)
            .options(selectinload(self.model.items))
        )
        orders = await self.session.execute(query)
        orders_data = orders.scalars().all()
        orders = []
        for order in orders_data:
            order_data = self.create_order_dto(order)
            orders.append(order_data)
        return orders

    async def update_one(
            self,
            order_id: int,
            data: dict
    ) -> OrderResponseDTO:
        query = (
            select(self.model)
            .options(selectinload(self.model.items))
            .where(self.model.id == order_id)
        )
        order = await self.session.execute(query)
        order = order.scalar_one()
        for key, value in data.items():
            if value is not None:
                setattr(order, key, value)
        await self.session.flush()
        order = self.create_order_dto(order)
        return order


    async def update_status(
            self,
            order_id: int,
            data: dict
    ) -> OrderResponseDTO:
        query = (
            select(self.model)
            .options(selectinload(self.model.items))
            .where(self.model.id == order_id)
        )
        order = await self.session.execute(query)
        order_data = order.scalar_one()
        order_data.status = data['status']
        order = self.create_order_dto(order_data)
        return order
