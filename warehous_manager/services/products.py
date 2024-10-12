from warehous_manager.dto.products import ProductCreateDTO, ProductUpdateDTO, ProductResponseDTO
from warehous_manager.repositories.products import ProductRepository


class ProductService:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    async def create(
            self,
            data: ProductCreateDTO
    ) -> ProductResponseDTO:
        return await self.product_repo.add_one(data=data)

    async def get(self, product_id: int) -> ProductResponseDTO:
        return await self.product_repo.get_one(
            product_id=product_id
        )

    async def get_all(self) -> list:
        products_data = await self.product_repo.get_objects()
        return products_data

    async def update(
            self,
            product_id: int,
            data: ProductUpdateDTO
    ) -> ProductResponseDTO:
        product = await self.product_repo.update_one(
            product_id=product_id,
            data=data
        )
        return product

    async def delete(self, product_id: int) -> None:
        await self.product_repo.delete_one(
            product_id=product_id
        )
