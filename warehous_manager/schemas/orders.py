from typing import Literal, List

from pydantic import BaseModel, ConfigDict

from warehous_manager.enams.statuses import Statuses
from warehous_manager.schemas.products import ProductsItemsSchema


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
