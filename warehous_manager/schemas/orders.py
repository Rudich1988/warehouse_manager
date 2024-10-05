from typing import Literal, List, Dict, Any
from datetime import datetime
from decimal import Decimal
from typing_extensions import Annotated

from pydantic import BaseModel, ConfigDict, PlainSerializer

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


CustomDecimal = Annotated[
    Decimal, PlainSerializer(lambda x: str(x), return_type=str, when_used='json')
]


class OrderResponseSchema(BaseModel):
    '''
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            Decimal: lambda v: float(v),
            datetime: lambda v: v.isoformat()
        }
    )
    '''

    id: int
    #created_at: datetime
    status: Literal[
        Statuses.IN_PROGRESS,
        Statuses.SENT,
        Statuses.DELIVERED
    ]
    items: list[OrderItemsSchema]
    order_cost: CustomDecimal
    product_count: int

    class Config:
        orm_mode = True
        from_attributes = True
        #json_encoders = {
         #   Decimal: lambda v: str(v),
            #datetime: lambda v: str(v)
        #}

OrderResponseSchema.model_rebuild()
