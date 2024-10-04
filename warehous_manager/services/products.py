from typing import List, Any

from warehous_manager.models.orders import Order
from warehous_manager.repositories.products import ProductRepository
from warehous_manager.schemas.products import ProductResponseSchema
from warehous_manager.schemas.order_items import OrderItemsSchema
from warehous_manager.schemas.orders import OrderResponseSchema
from warehous_manager.services.inventory_manager import InventoryManagerService


class ProductService:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    async def create(self, data: dict):
        product = await self.product_repo.add_one(data=data)
        print(product.id)
        product_data = ProductResponseSchema.from_orm(
            product
        ).model_dump()
        return product_data

    async def get(self, data):
        product = await self.product_repo.get_one(data=data)
        product_data = ProductResponseSchema.from_orm(
            product
        ).model_dump()
        product_data = ProductResponseSchema.from_orm(
            product
        ).model_dump()
        return product_data

    async def get_all(self):
        products = await self.product_repo.get_objects()
        products_data = [
            ProductResponseSchema.from_orm(
                product
            ).model_dump()
            for product in products
        ]
        return products_data

    async def update(self, product_id: int, data: dict):
        product = await self.product_repo.update_one(
            object_id=product_id,
            data=data
        )
        product_data = ProductResponseSchema.from_orm(
            product
        ).model_dump()
        return product_data

    async def delete(self, id: int):
        await self.product_repo.delete_one(data={'id': id})
        return f'product id: {id} deleted'

    async def add_products_to_order(
            self,
            data: List[str: Any]
    ):
        products_items = []
        for product_data in data:
            product = await self.product_repo.get_one(
                {'id': product_data['id']}
            )
            product.quantity -= product_data['quantity']
            products_items.append(
                {
                    'id': product.id,
                    'name': product.name,
                    'price': float(product.price),
                    'quantity': product_data['quantity']
                }
            )
        return products_items
