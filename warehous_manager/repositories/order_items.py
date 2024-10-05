from warehous_manager.utils.repository import SQLAlchemyRepository
from warehous_manager.models.order_items import OrderItem

class OrderItemsRepository(SQLAlchemyRepository):
    model = OrderItem
