from warehous_manager.repositories.orders import OrderRepository
from warehous_manager.schemas.orders import OrderResponseSchema
from warehous_manager.enams.statuses import Statuses
from warehous_manager.repositories.order_items import OrderItemsRepository
from warehous_manager.db.db import Session
from warehous_manager.repositories.products import ProductRepository
from warehous_manager.services.products import ProductService
from warehous_manager.services.inventory_manager import InventoryManagerService


class OrderService:
    def __init__(self, order_repo: OrderRepository):
        self.order_repo = order_repo

    async def create(self, data: dict, session: Session):
        inventory_manager = InventoryManagerService()
        product_count = inventory_manager.get_product_count(data['products'])
        order_data = {'status': Statuses.IN_PROGRESS, 'product_count': product_count}
        order = await self.order_repo.add_one(data=order_data)
        data['order_id'] = order.id
        orders_items = await OrderItemsRepository(
            session
        ).add_objects(data)
        products_data = inventory_manager.prepare_products_data(data['products'])
        products = await ProductRepository(session).update_objects(
            products_data['ids'],
            products_data['data']
        )
        order_data = inventory_manager.get_order_data(
            products=products,
            products_data=data['products']
        )
        order.order_cost = order_data['order_cost']
        order_data['id'] = data['order_id']
        order_data['created_at'] = str(order.created_at)
        order_data['status'] = order.status
        order_data['order_cost'] = float(order_data['order_cost'])
        return order_data


        #order = OrderResponseSchema.from_orm(
         #   order
        #).model_dump()
        #order['created_at'] = str(order['created_at'])
        #order['products'] = products_items
        #return order

    async def get(self, data: dict):
        order = await self.order_repo.get_one(data)
        #order_data = OrderResponseSchema.from_orm(
         #   order
        #)
        #items = order.items
        #print(items)
        print(order.items[0].product)
        return order
