from warehous_manager.utils.repository import SQLAlchemyRepository
from warehous_manager.models.order_items import OrderItem

class OrderItemsRepository(SQLAlchemyRepository):
    model = OrderItem

    async def add_objects(self, data: dict) ->None:
        objects = [self.model(**item) for item in data]
        self.session.add_all(objects)
        self.session.flush()
