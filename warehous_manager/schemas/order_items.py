from datetime import datetime
from decimal import Decimal
from typing_extensions import Annotated

from pydantic import BaseModel, ConfigDict, PlainSerializer

CustomDecimal = Annotated[
    Decimal, PlainSerializer(lambda x: str(x), return_type=str, when_used='json')
]


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
    product_price: CustomDecimal
    product_name: str

    class Config:
        orm_mode = True
        from_attributes = True
        '''
        json_encoders = {
            Decimal: lambda v: str(v),
            datetime: lambda v: str(v)
        }
        '''


OrderItemsSchema.model_rebuild()
