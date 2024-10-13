from warehous_manager.dto.orders import OrderCreateDTO, OrderResponseDTO
from warehous_manager.repositories.orders import OrderRepository
from warehous_manager.enams.statuses import Statuses
from warehous_manager.repositories.order_items import OrderItemsRepository
from warehous_manager.db.db import Session
from warehous_manager.repositories.products import ProductRepository
from warehous_manager.services.inventory_manager import InventoryManagerService


class OrderService:
    def __init__(self, order_repo: OrderRepository):
        self.order_repo = order_repo

    async def create(
            self,
            data: OrderCreateDTO,
            session: Session
    ) -> OrderResponseDTO:
        inventory_manager = InventoryManagerService()
        product_count = (inventory_manager
                         .get_product_count(data.products))
        order_data = {
            'status': Statuses.IN_PROGRESS,
            'product_count': product_count
        }

        order_id = await self.order_repo.add_one(data=order_data)

        data.order_id = order_id
        products_data = (inventory_manager
                         .prepare_products_data(data.products))

        products = await ProductRepository(session).update_products(
            products_data['ids'],
            products_data['data']
        )

        inventory_manager.check_products_existence(
            products=products,
            request_products=data.products
        )

        order_data = inventory_manager.get_order_data(
            products=products,
            data=data
        )

        await OrderItemsRepository(
            session=session
        ).add_objects(data=order_data['order_items'])

        order = await self.order_repo.update_one(
            order_id=order_id,
            data={'order_cost': order_data['order_cost']}
        )
        return order

    async def get(self, order_id: int) -> OrderResponseDTO:
        return await self.order_repo.get_one(order_id=order_id)


    async def update_order_status(
            self,
            order_id: int,
            status: str
    ) -> OrderResponseDTO:
        order = await self.order_repo.update_status(
            order_id=order_id,
            data={'status': status}
        )
        return order

    async def get_all(self) -> list:
        return await self.order_repo.get_objects()
