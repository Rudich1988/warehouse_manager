from pydantic import BaseModel, ConfigDict


class OrderItemsSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    product_id: int
    order_id: int
