import json

from warehous_manager.repositories.orders import OrderRepository
from warehous_manager.schemas.order_items import OrderItemsSchema
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
        products_data = inventory_manager.prepare_products_data(data['products'])
        products = await ProductRepository(session).update_objects(
            products_data['ids'],
            products_data['data']
        )
        order_data = inventory_manager.get_order_data(
            products=products,
            data=data
        )
        await OrderItemsRepository(
            session=session
        ).add_objects(data=order_data['order_items'])
        order.order_cost = order_data['order_cost']
        return


        #order_data['id'] = data['order_id']
        #order_data['created_at'] = str(order.created_at)
        #order_data['status'] = order.status
        #order_data['order_cost'] = float(order_data['order_cost'])
        print(order_data)
        return
        return order_data

    async def get(self, data: dict):
        data = await self.order_repo.get_one(data)
        order = OrderResponseSchema.from_orm(data[0].Order).json()
        return json.dumps(order)




        '''
        order = data[0].Order
        products = []
        for related_objects in data:
            order_item = OrderItemsSchema.from_orm(
                related_objects.OrderItem
            )
            products.append(order_item)
        order_data = OrderResponseSchema.from_orm(order)
        order_data.items = products
        return order_data
        '''
