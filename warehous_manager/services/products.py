from warehous_manager.repositories.products import ProductRepository
from warehous_manager.schemas.products import ProductResponseSchema


class ProductService:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    async def create(self, data: dict):
        product = await self.product_repo.add_one(data=data)
        product_data = ProductResponseSchema.from_orm(
            product
        ).model_dump()
        return product_data

    async def get(self, data):
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
