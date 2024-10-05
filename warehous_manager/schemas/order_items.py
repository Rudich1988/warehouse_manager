from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class OrderItemsSchema(BaseModel):
    '''
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders = {
            Decimal: lambda v: float(v)
        }
    )
    '''

    id: int
    product_id: int
    order_id: int
    quantity: int
    product_price: Decimal
    product_name: str

    class Config:
        orm_mode = True
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v),
            datetime: lambda v: v.timestamp()
        }


OrderItemsSchema.model_rebuild()
