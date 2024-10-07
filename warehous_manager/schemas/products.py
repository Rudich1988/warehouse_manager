from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class ProductsItemsSchema(BaseModel):
    model_config = ConfigDict(extra='forbid')

    id: int
    product_count: int


class ProductCreateSchema(BaseModel):
    model_config = ConfigDict(extra='forbid')

    name: str = Field(min_length=3)
    description: str = Field(min_length=3)
    price: Decimal = Field(ge=0)
    product_count: int = Field(ge=0)


class ProductUpdateSchema(BaseModel):
    model_config = ConfigDict(extra='forbid')

    name: Optional[str] = Field(None, min_length=3)
    description: Optional[str] = Field(None, min_length=3)
    price: Optional[float] = Field(None, ge=0)
    product_count: Optional[int] = Field(None, ge=0)
