from warehous_manager.repositories.orders import OrderRepository
from warehous_manager.schemas.orders import OrderResponseSchema
from warehous_manager.enams.statuses import Statuses
from warehous_manager.repositories.order_items import OrderItemsRepository
from warehous_manager.db.db import Session
from warehous_manager.repositories.products import ProductRepository
from warehous_manager.services.products import ProductService


class OrderService:
    def __init__(self, order_repo: OrderRepository):
        self.order_repo = order_repo

    async def create(self, data: dict, session: Session):
        order_data = {'status': Statuses.IN_PROGRESS}
        order = await self.order_repo.add_one(data=order_data)
        data['order_id'] = order.id
        orders_items = await OrderItemsRepository(
            session
        ).add_objects(data)
        #print(order.items)
        products_items = [
            product_item for product_item in await ProductService(
                ProductRepository(session=session)
            ).add_products_to_order(data=data['products'])
        ]
        order = OrderResponseSchema.from_orm(
            order
        ).model_dump()
        order['created_at'] = str(order['created_at'])
        order['products'] = products_items
        return order

    async def get(self, data: dict):
        order = await self.order_repo.get_one(data)
        #order_data = OrderResponseSchema.from_orm(
         #   order
        #)
        #items = order.items
        #print(items)
        print(order.items[0].product)
        return order
