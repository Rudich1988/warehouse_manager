from sqlalchemy import update, case

from warehous_manager.utils.repository import SQLAlchemyRepository
from warehous_manager.models.products import Product

class ProductRepository(SQLAlchemyRepository):
    model = Product

    async def update_objects(self, ids: list[int], data: dict):
        field_updates = {
            'quantity': case(
                *[(self.model.id == update_data['id'], self.model.quantity - update_data['quantity']) for update_data in data],
                else_=self.model.quantity
            ),
        }
        query = (
            update(self.model)
            .where(self.model.id.in_(ids))
            .values(field_updates)
            .returning(self.model.id, self.model.name, self.model.price)
        )
        products = await self.session.execute(query)
        return products.fetchall()
