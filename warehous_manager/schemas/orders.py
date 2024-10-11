from datetime import datetime
from typing import Literal, List

from pydantic import BaseModel, ConfigDict

from warehous_manager.enams.statuses import Statuses
from warehous_manager.schemas.products import ProductsItemsSchema
from warehous_manager.schemas.serializers import CustomDecimal
from warehous_manager.schemas.order_items import OrderItemsSchema


class OrderCreateSchema(BaseModel):
    model_config = ConfigDict(extra='forbid')

    products: List[ProductsItemsSchema]


class OrderUpdateStatusSchema(BaseModel):
    model_config = ConfigDict(extra='forbid')

    status: Literal[
    Statuses.IN_PROGRESS,
    Statuses.SENT,
    Statuses.DELIVERED
    ]


class OrderResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    status: Literal[
        Statuses.IN_PROGRESS,
        Statuses.SENT,
        Statuses.DELIVERED
    ]
    items: list[OrderItemsSchema]
    order_cost: CustomDecimal
    product_count: int


OrderResponseSchema.model_rebuild()
