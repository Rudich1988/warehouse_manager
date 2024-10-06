from warehous_manager.repositories.orders import OrderRepository
from warehous_manager.schemas.orders import OrderResponseSchema
from warehous_manager.enams.statuses import Statuses
from warehous_manager.repositories.order_items import OrderItemsRepository
from warehous_manager.db.db import Session
from warehous_manager.repositories.products import ProductRepository
from warehous_manager.services.inventory_manager import InventoryManagerService


class OrderService:
    def __init__(self, order_repo: OrderRepository):
        self.order_repo = order_repo

    async def create(self, data: dict, session: Session):
        inventory_manager = InventoryManagerService()
        product_count = (inventory_manager
                         .get_product_count(data['products']))
        order_data = {
            'status': Statuses.IN_PROGRESS,
            'product_count': product_count
        }

        order = await self.order_repo.add_one(data=order_data)

        data['order_id'] = order.id
        products_data = (inventory_manager
                         .prepare_products_data(data['products']))

        products = await ProductRepository(session).update_objects(
            products_data['ids'],
            products_data['data']
        )

        inventory_manager.check_products_existence(
            products=products,
            request_products=data['products']
        )

        order_data = inventory_manager.get_order_data(
            products=products,
            data=data
        )

        await OrderItemsRepository(
            session=session
        ).add_objects(data=order_data['order_items'])

        order.order_cost = order_data['order_cost']
        order = await self.get(data={'id': order.id})
        return order

    async def get(self, data: dict):
        order = await self.order_repo.get_one(data)
        order_data = OrderResponseSchema.from_orm(order)
        return order_data.model_dump(mode='json')

    async def update_order_status(self, order_id: int, status: str):
        order = await self.order_repo.get_one(data={'id': order_id})
        order.status = status
        order_data = await self.get(data={'id': order_id})
        return order_data

    async def get_all(self):
        orders = await self.order_repo.get_objects()
        orders_data = []
        for order in orders:
            orders_data.append(
                OrderResponseSchema.from_orm(order)
                .model_dump(mode='json')
            )
        return orders_data
