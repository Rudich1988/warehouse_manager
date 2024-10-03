from warehous_manager.utils.repository import SQLAlchemyRepository
from warehous_manager.models.products import Product

class ProductRepository(SQLAlchemyRepository):
    model = Product
