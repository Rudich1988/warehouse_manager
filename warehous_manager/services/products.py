from typing import List, Any

from warehous_manager.repositories.products import ProductRepository
from warehous_manager.schemas.products import ProductResponseSchema
from warehous_manager.db.db import Session


class ProductService:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    async def create(self, data: dict):
        product = await self.product_repo.add_one(data=data)
        product_data = ProductResponseSchema.from_orm(
            product
        ).model_dump()
        return product_data

    async def get(self, data: dict):
        product = await self.product_repo.get_one(data=data)
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
        '''
        если логика изменения количества товаров должна быть такой:
        мы должны указать насколько единиц должен быть изменено кол-во товара
        а не указываем количество товара. не знаю как правильно
        if data['quantity']:
            product = await self.product_repo.get_one(
                data={'id':product_id}
            )
            data['quantity'] += product.quantity
        '''
        product = await self.product_repo.update_one(
            product_id=product_id,
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
