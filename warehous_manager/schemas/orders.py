from typing import Literal, List, Dict, Any
from datetime import datetime, timedelta

from pydantic import BaseModel, ConfigDict

from warehous_manager.enams.statuses import Statuses
from warehous_manager.schemas.order_items import OrderItemsSchema


class OrderCreateSchema(BaseModel):
    model_config = ConfigDict(extra='forbid')

    products: List[Dict[str, Any]]


class OrderUpdateSchema(BaseModel):
    model_config = ConfigDict(extra='forbid')

    status: Literal[
    Statuses.SENT,
    Statuses.DELIVERED
    ]


class OrderResponseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.timestamp(),
        }
    )

    id: int
    status: Literal[
        Statuses.IN_PROGRESS,
        Statuses.SENT,
        Statuses.DELIVERED
    ]
    created_at: datetime

    #products: List[OrderItemsSchema]
