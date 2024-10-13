from sqlalchemy import update, case, select, delete
from dataclasses import asdict
from sqlalchemy.exc import NoResultFound

from warehous_manager.utils.repository import SQLAlchemyRepository
from warehous_manager.models.products import Product
from warehous_manager.dto.products import (
    ProductCreateDTO,
    ProductResponseDTO,
    ProductUpdateDTO
)
from warehous_manager.dto.order_items import MidDataItemsDTO

class ProductRepository(SQLAlchemyRepository):
    model = Product

    def create_product_dto(self, product):
        product_dto = ProductResponseDTO(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            product_count=product.product_count
        )
        return product_dto

    async def add_one(
            self,
            data: ProductCreateDTO
    ) -> ProductResponseDTO:
        product = self.model(
            **asdict(data, dict_factory=dict)
        )
        self.session.add(product)
        await self.session.flush()
        product_dto = self.create_product_dto(product)
        return product_dto

    async def get_one(
            self,
            product_id: int
    ) -> ProductResponseDTO:
        product = await self.session.execute(
            select(self.model).filter_by(id=product_id)
        )
        product_data = product.scalars().one()
        product_dto = self.create_product_dto(product_data)
        return product_dto

    async def get_objects(self) -> list:
        products = await self.session.execute(
            select(self.model))
        products = products.scalars().all()
        result = []
        for product in products:
            product_dto = self.create_product_dto(product)
            result.append(product_dto)
        return result


    async def update_one(
            self,
            product_id: int,
            data: ProductUpdateDTO
    ) -> ProductResponseDTO:
        fields = {}
        for key, value in asdict(
                data,
                dict_factory=dict
        ).items():
            if value:
                fields[key] = value
        stmt = (
            update(self.model)
            .where(self.model.id == product_id)
            .values(fields)
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        product = result.scalar_one()
        product_dto = self.create_product_dto(product)
        return product_dto


    async def delete_one(
            self,
            product_id: int,
    ) -> None:
        stmt = delete(self.model).where(self.model.id == product_id)
        result = await self.session.execute(stmt)
        if result.rowcount == 0:
            raise NoResultFound


    async def update_products(self, ids: list[int], data):
        field_updates = {
            'product_count': case(
                *[
                    (self.model.id == update_data.id,
                     self.model.product_count - update_data.product_count)
                    for update_data in data
                ],
                else_=self.model.product_count
            ),
        }
        query = (
            update(self.model)
            .where(self.model.id.in_(ids))
            .values(field_updates)
            .returning(
                self.model.id,
                self.model.name,
                self.model.price
            )
        )
        products = await self.session.execute(query)
        result = products.fetchall()
        products = []
        for product in result:
            products.append(
                MidDataItemsDTO(
                    id=product.id,
                    price=product.price,
                    name=product.name
                )
            )
        return products
