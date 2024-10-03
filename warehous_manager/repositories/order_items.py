from warehous_manager.utils.repository import SQLAlchemyRepository
from warehous_manager.models.order_items import OrderItem

class OrderItemsRepository(SQLAlchemyRepository):
    model = OrderItem

    async def add_objects(self, data):
        order_items = [
            self.model(
                **{key: value for key, value in item.items() if key != 'id'},
                product_id=item['id'],
                order_id=data['order_id']
            )
            for item in data['products']
        ]
        self.session.add_all(order_items)
        await self.session.flush()
        return order_items
