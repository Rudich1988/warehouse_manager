from pydantic import BaseModel, ConfigDict

from warehous_manager.schemas.serializers import CustomDecimal


class OrderItemsSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    quantity: int
    product_price: CustomDecimal
    product_name: str


OrderItemsSchema.model_rebuild()
